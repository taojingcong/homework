#include<iostream>
#include<fstream>
#define MAXSIZE1 100
#define MAXSIZE2 605
using namespace std;
int Min(int a,int b){
    if(a<b)
        return a;
    else
        return b;
}
int Max(int a,int b){
    if(a<b)
        return b;
    else
        return a;
}
void Knapsack(int m[][MAXSIZE2],int v[],int w[],int n,int c){
    int jMax=Min(w[n]-1,c);
    int i,j;
    for(j=0;j<=jMax;j++)//放不下第n个物品
        m[n][j]=0;
    for(j=w[n];j<=c;j++)//放得下第n个物品
        m[n][j]=v[n];
    
    for(i=n-1;i>1;i--){
        jMax=Min(w[i]-1,c);
        for(j=0;j<=jMax;j++)//放不下第i个物品
            m[i][j]=m[i+1][j];
        for(j=w[i];j<=c;j++)
            m[i][j]=Max(m[i+1][j],m[i+1][j-w[i]]+v[i]);
        m[1][c]=m[2][c];
        if(c>=w[1])
            m[1][c]=Max(m[2][c],m[1][c-w[1]]+v[1]);
    }
}
void TraceBack(int m[][MAXSIZE2],int w[],int c,int x[],int n){
    for(int i=1;i<n;i++){
        if(m[i][c]==m[i+1][c])
            x[i]=0;
        else{
            x[i]=1;
            c-=w[i];
        }
    }
    x[n]=(m[n][c]>0)?1:0;
}
int main(){
    ifstream fptr;
    int m1[MAXSIZE1][MAXSIZE2],m2[MAXSIZE1][MAXSIZE2];
    int v1[MAXSIZE1],w1[MAXSIZE1],v2[MAXSIZE1],w2[MAXSIZE1];
    int c1,c2;//容量
    int x1[MAXSIZE1],x2[MAXSIZE1];
    int i;
    fptr.open("背包数据.txt");
    char str1[7],str2,str3[2];
    fptr>>str1;
    //cout<<str1<<endl;
    for(i=1;i<11;i++)
        fptr>>str2;
    fptr>>c1;
    fptr>>str3;
    
    for(i=1;i<11;i++)
        fptr>>str2;
    for(i=1;i<=50;i++)
        fptr>>w1[i];
    for(i=1;i<11;i++)//
        fptr>>str2;
    for(i=1;i<=50;i++)
        fptr>>v1[i];
    
    fptr>>str1;
    //cout<<str1<<endl;
    for(i=1;i<9;i++)
        fptr>>str2;
    fptr>>c2;
    //cout<<c2<<endl;
    fptr>>str3;
    
    for(i=1;i<11;i++)
        fptr>>str2;
    for(i=1;i<=99;i++)
        fptr>>w2[i];
    for(i=1;i<11;i++)//
        fptr>>str2;
    for(i=1;i<=99;i++)
        fptr>>v2[i];
    Knapsack(m1,v1,w1,50,c1);
    TraceBack(m1,w1,c1,x1,50);
    int sum1=0,sum2=0,value1=0,value2=0;
    for(i=1;i<=50;i++){
        if(x1[i]==1){
            sum1+=w1[i];
            value1+=v1[i];
        }
    }
    cout<<"背包1总重量为"<<sum1<<endl;
    cout<<"总价值为"<<value1<<endl;
    cout<<"放入的物品为"<<endl;
    for(i=1;i<=50;i++)
        if(x1[i]==1)
            cout<<"第"<<i<<"个物品"<<"    "<<"重量"<<w1[i]<<"    "<<"价值"<<v1[i]<<endl;
    cout<<endl;
    Knapsack(m2,v2,w2,99,c2);
    TraceBack(m2,w2,c2,x2,99);
    for(i=1;i<=99;i++){
        if(x2[i]==1){
            sum2+=w2[i];
            value2+=v2[i];
        }
    }
    cout<<"背包2总重量为"<<sum2<<endl;
    cout<<"总价值为"<<value2<<endl;
    cout<<"放入的物品为"<<endl;
    for(i=1;i<=99;i++)
        if(x2[i]==1)
            cout<<"第"<<i<<"个物品"<<"    "<<"重量"<<w2[i]<<"    "<<"价值"<<v2[i]<<endl;
    return 0;
}
