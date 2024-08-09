#include <bits/stdc++.h>
using namespace std;
int main()
{
    int n,target;
    bool flag = false;
    cin >> n;
    int enrg_arr[n];
    for(int i = 0 ; i < n ; i++)
    {
        cin >> enrg_arr[i];
    }
    cin >> target;
    for (int i = 0 ; i < n ; i++)
    {
        if (enrg_arr[i] == target)
        {
            cout << i;
            flag = true;
            break;
        }
    }
    if (!flag)
    {
        cout << -1;
    }
}
