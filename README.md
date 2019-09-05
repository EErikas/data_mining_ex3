# data_mining_ex3
Individual assignment for Data Mining Technologies at Vilnius University Kaunas Faculty. Assignment includes two parts: decsion tree creator and LIthuanian personal and corporate ID detection

## Decision tree
This page allows user to upload .csv formatted data and create decission trees using parameters listed on a page

## Lithuanian ID carver
This page detects corporate and personal Lithuanian IDs in the entered text
### Personal IDs
The personal code consists of 11 digits, for example: 33309240064:

the first shows the centenary of birth and the gender of the person (1 - 19th century male, 2 - 19th century female, 3 - 20th century male, 4 - 20th century female, 5 - 21st century male, 6 - 21st Century Woman);
the next six are the last two digits of the person's year of birth, month (two digits), day (two digits);
the next three digits are the number of those born on that day;
the last one is a check digit derived from other digits.
If the personal code is written ABCDEFGHIJK:

S = A * 1 + B * 2 + C * 3 + D * 4 + E * 5 + F * 6 + G * 7 + H * 8 + I * 9 + J * 1

The sum S is divided by 11, and if the remainder is not equal to 10, it is the control number K. If the remainder is 10, a new sum is calculated with the following weighting factors:

S = A * 3 + B * 4 + C * 5 + D * 6 + E * 7 + F * 8 + G * 9 + H * 1 + I * 2 + J * 3

This sum S is again divided by 11, and if the remainder is not equal to 10, it is a control number K. If the remainder is 10, the control number K is 0.
### Corporate IDs:
Corporate IDs consist of 7 or 9 digits and their validity is checked by searching for them in the Lithuanian Cenre of Registers

Working example can be found here: <https://ee-data-mining-lab.herokuapp.com>
