
#include <stdio.h>

const int OROCK[3] = { 3, 6, 0 };
const int OPAPE[3] = { 0, 3, 6 };
const int OSCIS[3] = { 6, 0, 3 };
const int SCORES[3] = { 1, 2, 3 };

int main(void) {
    // Read in input until EOF
    char opp, me;
    int score = 0;
    while (scanf("%c %c\n", &opp, &me) != EOF) {
        // Get the index of the opponent's move
        me = me - 'X' + 1;
        if (opp == 'A') {
            score += me + OROCK[me - 1];
        } else if (opp == 'B') {
            score += me + OPAPE[me - 1];
        } else if (opp == 'C') {
            score += me + OSCIS[me - 1];
        }
    }

    // Print the score
    printf("%d\n", score);
}