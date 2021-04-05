from app.models import Bill


def test_bill(test_client, database):
    b1 = Bill(amount=10, invoice="Dummy Bill")
    database.session.add(b1)
    database.session.commit()
    b2 = Bill.query.filter_by(amount=10).first()
    b3 = Bill.query.filter_by(invoice="Dummy Bill").first()
    
    '''
    To check that object is created aproperly and correcty returned on being filtered by amount
    assert b2.amount == 10
    assert b2.invoice == "Dummy Bill"
    To check that object is created aproperly and correcty returned on being filtered by invoice
    assert b3.amount == 10
    assert b3.invoice == "Dummy Bill"
    '''
    assert b2.amount == 10
    assert b2.invoice == "Dummy Bill"
    assert b3.amount == 10
    assert b3.invoice == "Dummy Bill"