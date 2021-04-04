from app.models import Bill


def test_bill(test_client, database):
    b1 = Bill(amount=10, invoice="Dummy Bill")
    database.session.add(b1)
    database.session.commit()
    b2 = Bill.query.filter_by(invoice="Dummy Bill").first()
    assert b2.amount == 10
    assert b2.invoice == "Dummy Bill"
