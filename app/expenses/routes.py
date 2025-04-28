from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Expense
from app.forms import ExpenseForm
from datetime import datetime

expenses = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses.route('/dashboard')
@login_required
def dashboard():
    mes = request.args.get('mes', None, type=int) or datetime.utcnow().month
    expenses_list = (
        Expense.query
               .filter_by(user_id=current_user.id)
               .filter(db.extract('month', Expense.vencimento) == mes)
               .order_by(Expense.vencimento)
               .all()
    )

    total = sum(e.valor for e in expenses_list)

    return render_template(
        'expenses/dashboard.html',
        expenses=expenses_list,
        mes=mes,
        total=total
    )

@expenses.route('/add', methods=['GET','POST'])
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


@expenses.route('/toggle/<int:id>')  
@login_required
def toggle_status(id):
    exp = Expense.query.get_or_404(id)
    exp.status = 'Pago' if exp.status == 'A pagar' else 'A pagar'
    db.session.commit()
    return redirect(url_for('expenses.dashboard', mes=request.args.get('mes')))

@expenses.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    exp = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(exp)
    db.session.commit()
    flash('Conta excluída com sucesso.', 'warning')
    return redirect(url_for('expenses.dashboard', mes=request.args.get('mes')))