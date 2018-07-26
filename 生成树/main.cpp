#include <iostream>
#include<fstream>
using namespace std;
typedef struct {
    int num;
    int id;
}station;
#define VNUM 22
//#define VNUM 42
#define INF 10000.0
int trans(station *node, int num)
{
    int i = 0;
    for (i = 1;i <= VNUM;i++)
    {
        if (node[i].num == num)return node[i].id;
    }
    return -1;
}
double prim(station *node,int n,double dist[][VNUM+1]) {
    int pre_point;
    double min, all_sum = 0.0;
    double distance_low[VNUM + 1];
    int visited[VNUM + 1];
    int i = 0, j = 0,temp = 0;
    visited[1] = 1;
    for (i = 2;i <= n;i++)visited[i] = 0;
    pre_point = 1;
    for (int i = 2; i <= n; i++){
        if (dist[pre_point][i] == 0)distance_low[i] = INF;
        else distance_low[i] = dist[pre_point][i];
    }
    int path[VNUM + 1][2];
    int num = 1;int flag = 0;
    for (int i = 1; i <= n - 1; i++) {
        min =INF;
        for (int j = 1; j <= n; j++) {
            if (visited[j] == 0 && min > distance_low[j]) {
                min = distance_low[j];
                pre_point = j;
            }
        }
        for (int k = 1;k <= n;k++)
        {
            if (visited[k] == 1 && min == dist[pre_point][k])
            {
                path[num][1] = pre_point;
                path[num][0] = k;
                num++;
            }
        }
        visited[pre_point] = 1;
        all_sum+= min;
        for (int j = 1; j <= n; j++) {
            if (visited[j] == 0 && distance_low[j] > dist[pre_point][j])
                if (dist[pre_point][j]!=0)distance_low[j]=dist[pre_point][j];
        }
    }
    
    for (int i = 1;i < num;i++)
    {
        int a = path[i][0];
        int b = path[i][1];
        cout << "基站" <<trans(node,a)<<'('<<a<<')'<< "  基站" << trans(node, b) << '(' << b << ')'<< endl;
    }
    return all_sum;
}
int main()
{
    double dist[VNUM+1][VNUM+1];
    fstream f;
    int i = 0, j = 0;
    f.open("22-1.txt");
    if (f)
    {
        for (i = 1;i <= VNUM;i++)
        {
            for (j = 1;j <= VNUM;j++)
            {
                f >> dist[i][j];
                if (dist[i][j] < 0)
                    dist[i][j] = 0;
                
            }
        }
        f.close();
        f.open("22-2.txt");
        station node[VNUM + 1];
        int num[VNUM + 1];
        if (f)
        {
            for (i = 1;i <= VNUM;i++)
            {
                f >> node[i].id;
                node[i].num = i;
            }
        }
        double sum = prim(node,VNUM, dist);
        cout << "总权值为："<<sum;
    }
    else {
        cout << "error";
    }
    system("pause");
    
}

