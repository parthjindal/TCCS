from app.models import Bill

def test_bill(test_client, database):
    b1 = Bill(amount = 10, paymentID = "10AY20")
    database.session.add(b1)
    database.session.commit()
    b2 = Bill.query.filter_by(paymentID = "10AY20").first()
    assert b2.amount == 10
    assert b2.paymentID == "10AY20"