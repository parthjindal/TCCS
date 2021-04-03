from app.models import Bill

def test_bill():
    b1 = Bill(amount = 10, paymentID = "10AY20")
    assert b1.amount == 10
    assert b1.paymentID == "10AY20"