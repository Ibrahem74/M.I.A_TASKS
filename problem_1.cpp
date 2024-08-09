#include <bits/stdc++.h>
using namespace std;
int main()
{
    int rows,aster_count=1;
    cin >> rows;
    for (int row_number = 0 ; row_number < rows ; row_number++)
    {
        for (int aster_number = 0 ; aster_number < aster_count ; aster_number++)
        {
            cout <<"*";
        }
        if(row_number != rows-1)
        {
            cout <<"\n";
        }
        aster_count++;
    }
}
