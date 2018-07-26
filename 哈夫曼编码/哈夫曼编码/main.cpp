//
//  main.cpp
//  哈夫曼编码
//
//  Created by 陶靖枞 on 2018/6/8.
//  Copyright © 2018年 陶靖枞. All rights reserved.
//

#include <iostream>
#include<fstream>
#include<queue>
using namespace std;
char huf[30];
int result=0;
int res=0;
char ch[28]={'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','#'};
typedef struct node{
    char c;
    int weight;
    node* right,*left,*self;
    friend bool operator<(const node &a,const node &b){
        return a.weight>b.weight;
    }
}node;
priority_queue<node> p;
void openfile(int *a){
    ifstream file("哈夫曼编码输入文本.txt");
    if(!file.is_open())cout<<"打开文本失败\n";
    char s[2100];
    file>>s;
    int length1=strlen(s);
    cout<<length1<<endl;
    int i=0,j=0,k;
    while(i<length1){
        for(j=0,k=0;j<=27&&k==0;j++){
            if(s[i]==ch[j]){
                k=1;
                a[j]=a[j]+1;
            }
        }
        i++;
    }
}
void dfs(node* root,int level){//深度遍历二叉树的叶子结点
   
   if(root->left==root->right){
        huf[level]='\0';
        printf("%c的编码: %s,%d位,频率%d\n",root->c,huf,strlen(huf),root->weight);
        result=result+strlen(huf)*root->weight;
    }
   else{
        huf[level]='0';
        dfs(root->left,level+1);
        huf[level]='1';
        dfs(root->right,level+1);
   }
}
void huffuman(int* a){//建立哈夫曼编码的二叉树
    node *root,fir,sec;
    for(int i=0;i<28;i++){//对每个字符生成一个节点，并压入队列
        if(a[i]!=0){
        root=(node*)malloc(sizeof(node));
        root->c=ch[i];
        root->weight=a[i];
        root->left=root->right=NULL;
        root->self=root;
        p.push(*root);
        }
    }
    while(p.size()>1){//每次选择最小的两个节点，合并
        fir=p.top();p.pop();
        sec=p.top();p.pop();
       // cout<<"fir:"<<fir.weight<<"sec:"<<sec.weight<<endl;
        root=(node*)malloc(sizeof(node));
        root->left=fir.self;
        root->right=sec.self;
        root->self=root;
        root->weight=fir.weight+sec.weight;
        p.push(*root);
    }
    fir=p.top();
    p.pop();
    cout<<1<<endl;
    dfs(fir.self, 0);
}

int main(int argc, const char * argv[]) {
    int a[28]={0};
    openfile(a);
    huffuman(a);
    cout<<result<<endl;
    return 0;
}
