#include<iostream>
using namespace std;

template<class a>
class A: public a{
    int x;
    A();
};
class b{
    public:
    int x;
};

int main(){
    b x;

    A<b> y;
    y.x = 10;
    cout << y.x;
}
