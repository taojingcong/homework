//
//  main.cpp
//  最短路径
//
//  Created by 陶靖枞 on 2018/6/11.
//  Copyright © 2018年 陶靖枞. All rights reserved.
//

#include <iostream>
#include<fstream>
#include <sstream>
using namespace std;
#define VNUM 22
float arcs[VNUM][VNUM];
string v_name[VNUM];
#define v0 19
void int2str(const int &int_temp,string &string_temp)
{
    stringstream stream;
    stream<<int_temp;
    string_temp=stream.str();   //此处也可以用 stream>>string_temp
}
void openfile(){
    int num=VNUM;
    ifstream file("42点名.txt");
    for(int i=0;i<num;i++){
        file>>v_name[i];
    }
    ifstream ac("42矩阵.txt");
    for(int i=0;i<num;i++){
        for(int j=0;j<num;j++){
            ac>>arcs[i][j];
            if(arcs[i][j]==-1){
                arcs[i][j]=10000;
            }
        }
        //cout<<endl;
    }
}
int main(int argc, const char * argv[]) {
    openfile();
    int path,point,count;
    string p[VNUM];
    int i, pre[VNUM];;
    float min;
    string s;
    int w;
    int v=0;
    float D[VNUM];
    int VS[VNUM];
    for(v=0;v<VNUM;v++){
        VS[v]=0;
        D[v]=arcs[v0][v];
        if(D[v]<10000)pre[v]=v0;
    }
    
    D[v0]=0;
    VS[v0]=1;
    for(i=1;i<VNUM;i++){
        min=10000;
        for(w=0;w<VNUM;w++){//选取在s外最近的点
            if(VS[w]==0)
                if(D[w]<min){
                    min=D[w];v=w;
                }
        }
        VS[v]=1;
        for(w=0;w<VNUM;w++){
           if(VS[w]==0&&(min+arcs[v][w]<D[w])){
               D[w]=min+arcs[v][w];
               pre[w]=v;
           }
        }

    }
    for(i=0;i<VNUM;i++)if(D[i]<10000){
        point=i;
        count=1;
        p[0]=v_name[i];
        while(point!=v0){
            path=pre[point];
            //cout<<v_name[path]<<" ";
            p[count]=v_name[path];
            point=path;
            count++;
        }
        count--;
        cout<<" 从v0到"<<v_name[i]<<"个点的最短路径为 "<<D[i]<<endl;
        while(count!=0){
            cout<<p[count]<<"->";
            count--;
        }
        cout<<p[count];
        cout<<endl;
    }
    
    return 0;
}






