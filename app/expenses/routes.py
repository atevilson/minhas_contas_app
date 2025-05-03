from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Expense
from app.forms import ExpenseForm
from datetime import datetime

bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@bp.route('/dashboard')
@login_required
def dashboard():
    mes = request.args.get('mes', None, type=int) or datetime.utcnow().month
    ano  = request.args.get('ano',  None, type=int) or datetime.utcnow().year

    expenses_list = (
        Expense.query
               .filter_by(user_id=current_user.id)
               .filter(db.extract('month', Expense.vencimento) == mes)
               .filter(db.extract('year', Expense.vencimento) == ano)
               .order_by(Expense.vencimento)
               .all()
    )

    total = sum(e.valor for e in expenses_list)

    return render_template(
        'expenses/dashboard.html',
        expenses=expenses_list,
        mes=mes,
        ano=ano,
        total=total
    )

@bp.route('/add', methods=['GET','POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        base_date = form.vencimento.data
        total     = form.valor.data
        num_parc  = form.parcelas.data

        if num_parc == 0:
            exp = Expense(
                origem        = form.origem.data,
                vencimento    = base_date,
                valor         = total,
                status        = form.status.data,
                quem_paga     = form.quem_paga.data,
                tipo          = form.tipo.data,
                parcelas      = 0,
                parcel_number = 0,
                owner         = current_user
            )
            db.session.add(exp)
        else:
            per_valor = total / num_parc
            for i in range(1, num_parc + 1):
                offset = base_date.month - 1 + (i - 1)
                year   = base_date.year + offset // 12
                month  = offset % 12 + 1
                day    = min(base_date.day, 28)
                venc   = base_date.replace(year=year, month=month, day=day)

                exp = Expense(
                    origem        = form.origem.data,
                    vencimento    = venc,
                    valor         = per_valor,
                    status        = form.status.data,
                    quem_paga     = form.quem_paga.data,
                    tipo          = form.tipo.data,
                    parcelas      = num_parc,
                    parcel_number = i,
                    owner         = current_user
                )
                db.session.add(exp)

        db.session.commit()
        flash('Conta adicionada com sucesso!', 'success')
        return redirect(url_for('expenses.dashboard', mes=base_date.month))

    return render_template('expenses/add.html', form=form)


@bp.route('/toggle/<int:id>')  
@login_required
def toggle_status(id):
    exp = Expense.query.get_or_404(id)
    exp.status = 'Pago' if exp.status == 'A pagar' else 'A pagar'
    db.session.commit()
    return redirect(url_for('expenses.dashboard', mes=request.args.get('mes')))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    mes = request.args.get('mes', 1, type=int)
    debt = Expense.query.get_or_404(id)
    origem = debt.origem
    total_parcelas = debt.parcelas

    deleted = Expense.__table__.delete().where(
        (Expense.origem == origem) &
        (Expense.parcelas == total_parcelas)
    )

    db.session.execute(deleted)

    db.session.commit()
    flash(f'Todas as {total_parcelas} parcelas de "{origem}" foram excluídas.', 'warning')
    return redirect(url_for('expenses.dashboard', mes=mes))

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    mes  = request.args.get('mes', 1, type=int)
    debt = Expense.query.get_or_404(id)
    form = ExpenseForm(obj=debt)

    if request.method == 'GET': # para trazer no campo Valor total a soma das parcelas
        total = debt.valor * (debt.parcelas or 1) 
        form.valor.data = total

    if form.validate_on_submit():
        orig       = debt.origem
        parc       = debt.parcelas
        user       = current_user

        base_date  = form.vencimento.data
        total      = form.valor.data
        num_parc   = form.parcelas.data

        if num_parc != parc:
            delete_conta_atual = Expense.__table__.delete().where(
                (Expense.user_id == user.id) &
                (Expense.origem == orig) &
                (Expense.parcelas == parc)
            )
            db.session.execute(delete_conta_atual)
            db.session.commit()

            if num_parc == 0:
                nova = Expense(
                    origem        = form.origem.data,
                    vencimento    = base_date,
                    valor         = total,
                    status        = form.status.data,
                    quem_paga     = form.quem_paga.data,
                    tipo          = form.tipo.data,
                    parcelas      = 0,
                    parcel_number = 0,
                    owner         = user
                )
                db.session.add(nova)
            else:
                per_valor = total / num_parc
                for i in range(1, num_parc + 1):
                    offset = base_date.month - 1 + (i - 1)
                    year   = base_date.year + offset // 12
                    month  = offset % 12 + 1
                    day    = min(base_date.day, 28)
                    venc   = base_date.replace(year=year, month=month, day=day)

                    parcela = Expense(
                        origem        = form.origem.data,
                        vencimento    = venc,
                        valor         = per_valor,
                        status        = form.status.data,
                        quem_paga     = form.quem_paga.data,
                        tipo          = form.tipo.data,
                        parcelas      = num_parc,
                        parcel_number = i,
                        owner         = user
                    )
                    db.session.add(parcela)

            flash(f'A conta "{form.origem.data}" foi recriada em {num_parc or 1} parcela(s).', 'success')

        else:
            serie = Expense.query.filter_by(
                user_id=user.id,
                origem=orig,
                parcelas=parc
            ).all()

            per_valor = (total / parc) if parc > 0 else total
            for e in serie:
                e.origem    = form.origem.data
                e.valor     = per_valor
                e.status    = form.status.data
                e.quem_paga = form.quem_paga.data
                e.tipo      = form.tipo.data

            flash(f'A conta "{form.origem.data}" foi atualizada em todas as {parc or 1} parcela(s).', 'success')

        db.session.commit()
        return redirect(url_for('expenses.dashboard', mes=base_date.month))

    return render_template(
        'expenses/add.html',
        title="Editar conta",
        form=form,
        submit_label="Salvar alterações"
    )