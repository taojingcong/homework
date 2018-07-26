
#include<fstream>
#include <iostream>
#include<time.h>
using namespace std;
#define vnum 21
#define inf 99999
int v_name[vnum];
float map[vnum][vnum];
int x[vnum],cw,bestx[vnum],node_num;
float bestw;
void swap(int &a,int &b){
    int c=a;
    a=b;
    b=c;
}
void openfile(){
    fstream file("1.txt");
    fstream name("2.txt");
    int i,j;
    for(i=1;i<vnum;i++){
        for(j=1;j<vnum;j++){
            file>>map[i][j];
        }
    }
    for(i=1;i<vnum;i++){
        name>>v_name[i];
    }
    file.close();
    name.close();
}
void backtracTSP(int i){
    node_num++;
    int n=vnum-1,j;
    if(i==n){
        if(map[x[n-1]][x[n]]!=inf&&map[x[n]][x[1]]!=inf){
            if(cw+map[x[n-1]][x[n]]+map[x[n]][x[1]]<bestw){
               bestw=cw+map[x[n-1]][x[n]]+map[x[n]][x[1]];
               for(j=1;j<=n;j++)bestx[j]=x[j];
            }
        }
    }
    else{
      for(j=i;j<=n;j++){
        if(map[x[i-1]][x[j]]!=inf&&cw+map[x[i-1]][x[j]]<bestw){
            swap(x[i],x[j]);
            cw=cw+map[x[i-1]][x[i]];
            backtracTSP(i+1);
            cw=cw-map[x[i-1]][x[i]];
            swap(x[i],x[j]);
        }
      }
    }
}
int main(int argc, const char * argv[]) {
    clock_t start,finish;
    double totaltime;
    start=clock();

    int i;
    cw=0;node_num=0;
    bestw=99999;
    for(i=1;i<vnum;i++)x[i]=i;
    swap(x[18],x[1]);
    openfile();
    backtracTSP(2);
    bestw=0;
    cout<<"最优路径为:";
    for(i=1;i<vnum-1;i++){
        cout<<v_name[bestx[i]]<<"->";
        bestw=bestw+map[bestx[i]][bestx[i+1]];
    }
    bestw=bestw+map[bestx[i]][bestx[1]];
    cout<<endl;
    cout<<"树节点数:"<<node_num<<" 路径总长度:"<<bestw<<endl;;
    finish=clock();
    totaltime=(double)(finish-start)/CLOCKS_PER_SEC;
    cout<<"\n此程序的运行时间为"<<totaltime<<"秒！"<<endl;

    return 0;
}
