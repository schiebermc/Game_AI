/*
    Battleship Game AI by Matthew Schieber
    All implementations were concieved and iterated by me.
    Please make any suggestions at https://github.com/schiebermc/Game_AI
*/

#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include <math.h>
#include <cmath>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <climits>
#include <float.h>
#include <bitset>

using namespace std;

typedef pair<int, int> xy;

class Move : xy {
public:
    Move(xy p) : xy(p) {} 
    void perform_move() {cout << this->first << ' ' << this->second << endl;}  
};

class Moves : public vector<Move> {

    // class for vector of moves. allows for name
    // contraction and an operator overload for ease of use.

public:

    void operator +=(Moves B) {
        for(Move& this_move : B) {
            this->push_back(this_move);
        }        
    }
};


class Board {

private:
    int n_;
    vector<vector<char>> board_;

public:
    
    Board() {}
    Board(int n) {n_ = n;}
    void read_board() {
        board_.resize(n_);
        for(int i=0; i<n_; i++) {
            board_[i].resize(n_);
            for(int j=0; j<n_; j++) {
                cin >> board_[i][j];
            }
        }
    }

    vector<vector<char>> get_board() {return board_;}
    int get_n() { return n_;}
    
};

class Player {

protected:
    Board board_;
    int n_;

public:
    
    Player(Board b) {
        board_ = b;
        n_ = b.get_n();
    }
    
    Moves get_legal_moves() {
        auto b = board_.get_board();
        Moves moves;
        for(int i=0; i<n_; i++) {
            for(int j=0; j<n_; j++) {
                char c = b[i][j];
                if(c == '-') {
                    moves.push_back(Move({i, j}));
                }
            }
        }
        return moves;
    }

    Move virtual get_best_move() {
        return Move({-1, -1});
    }

    void move() {
        get_best_move().perform_move();
    }

    friend class RandomPlayer;
};


class RandomPlayer : public Player {

public:
    
    RandomPlayer(Board b) : Player(b) {
    }

    Move get_random_move() {
        auto moves = get_legal_moves();
        return moves[rand() % moves.size()];
    }

    Move virtual get_best_move() {
        return get_random_move();
    }

};

class BetterPlayer : public RandomPlayer {

    // I'm calling it Better, bc no minimax is necessary..

public:
    
    BetterPlayer(Board b) : RandomPlayer(b) {
    }

    Move virtual get_best_move() {

        // get all moves that hit
        set<xy> hits;
        auto b = board_.get_board();
        for(int i=0; i<n_; i++) {
            for(int j=0; j<n_; j++) {
                char c = b[i][j];
                if(c == 'h') {
                    xy p = {i, j};
                    hits.emplace(p);
                }
            }
        }

        // if no hits, go random        
        if(hits.size() == 0) {
            return get_random_move();
        } 

        // otherwise, add some intelligence
        // we first check all hit points with an aggresive tactic
        // we should only fall back on the non-aggressive tactic if
        // there exists no aggresive moves. 
        Moves moves;
        for(auto p : hits) {
            moves += get_possible_moves_hits_from_here(p, 1);
        }  
    
        if(moves.size() == 0) {
            for(auto p : hits) {
                moves += get_possible_moves_hits_from_here(p, 0);
            }  
        }
       
        return moves[rand() % moves.size()];
    }

    Moves get_possible_moves_hits_from_here(xy pos, bool aggressive) {
        
        // should be trajectory based
        Moves moves_from_here;
        
        // check vertically
        xy up   = {pos.first - 1, pos.second};  
        xy down = {pos.first + 1, pos.second};  
        moves_from_here += split_moves(up, down, aggressive);
        
        // check horizontally
        xy left  = {pos.first, pos.second - 1};  
        xy right = {pos.first, pos.second + 1};  
        moves_from_here += split_moves(left, right, aggressive);
 
        return moves_from_here;
    }

    Moves split_moves(xy p1, xy p2, bool aggressive) {
        
        Moves moves_from_here;
        int r1 = test_hit(p1); 
        int r2 = test_hit(p2); 
    
        // best scenarios are where one is a hit and the
        // other has not been check. cleary, add the one that
        // has not been checked
        if(r1 == 0 and r2 == 1) {
            moves_from_here.push_back(p1);
        } else if (r1 == 1 and r2 == 0) {
            moves_from_here.push_back(p2);
        } 

        // otherwise, just try one that hasn't been checked
        else if (not aggressive and r1 == 0) {
            moves_from_here.push_back(p1);
        }

        else if(not aggressive and r2 == 0) {
            moves_from_here.push_back(p2);

        }

        return moves_from_here;
     }

    int test_hit(xy pos) {
        // Returns:
        //  -1 if out of bounds
        //  0 if not checked
        //  1 if hit
        //  2 if nothing

        auto b = board_.get_board();
        if(pos.first < 0 or pos.first >= n_ or
           pos.second < 0 or pos.second >= n_) {
            return -1;
        }
        char c = b[pos.first][pos.second];
        if(c == '-') {
            return 0;
        } else if (c == 'h') {
            return 1;
        } else {
            return 2;
        }
    }
};

class ProbabilityPlayer : public RandomPlayer {

private:
    bool debug_ = false;

public:
    
    ProbabilityPlayer(Board b) : RandomPlayer(b) {
    }

    Move virtual get_best_move() {
        set<xy> hits;
        auto b = board_.get_board();
        vector<vector<float>> probs(n_);
        for(int i=0; i<n_; i++) {
            probs[i].resize(n_);
            for(int j=0; j<n_; j++) {
                char c = b[i][j];
                probs[i][j] = 0;
                if(c == '-') {
                    probs[i][j] = 5;
                    probs[i][j] += bump_all({i, j}, b);
                }
            }
        }

        if(debug_) {
            for(int i=0; i<n_; i++) {
                for(int j=0; j<n_; j++) {
                    printf("%.3f ", probs[i][j]);
                }
                printf("\n");
            }    
        }

        Move best_move({-1, -1});
        int best_util = -1;
        for(int i=0; i<n_; i++) {
            for(int j=0; j<n_; j++) {
                int p = probs[i][j];
                if(p > best_util) {
                    xy pos = {i, j};
                    best_move = Move(pos);
                    best_util = probs[i][j];
                } 
            }
        }
        return best_move;
    }
    

    int bump_all(xy pos, vector<vector<char>> board) {
    
        if(debug_) {    
            printf("testing: %d, %d\n", pos.first, pos.second);
        }
        
        //horizontal
        xy up1   = {pos.first - 1, pos.second};  
        xy up2   = {pos.first - 2, pos.second};  
        xy down1 = {pos.first + 1, pos.second};  
        xy down2 = {pos.first + 2, pos.second};  
        int ans = bump_all_split(up1, up2, down1, down2);
    
        // vertical
        xy left1  = {pos.first, pos.second - 1};  
        xy left2  = {pos.first, pos.second - 2};  
        xy right1 = {pos.first, pos.second + 1};  
        xy right2 = {pos.first, pos.second + 2};  
        ans += bump_all_split(left1, left2, right1, right2);
        
        if(debug_) {
            printf("\n");
        }
        return ans; 
    }

    // this is super sloppy, please forgive me coding gods
    int bump_all_split(xy p1, xy p3, xy p2, xy p4) {
        int r1 = test_hit(p1); 
        int r2 = test_hit(p2); 
        int r3 = test_hit(p3); 
        int r4 = test_hit(p4); 
        int ans = 0;

        if(debug_) {      
            printf("%d, %d, %d, %d\n", r1, r3, r2, r4);
        }

        // highst precedence - we have two in one direction
        if((r1 == 1 and r3 == 1) or
            (r2 == 1 and r4 == 1)) {
            ans += 10;
        
        }
        
        else {
            ans += (r1 == 1 ? 4 : 0);
            ans += (r2 == 1 ? 4 : 0);
            ans += (r1 == 2 ? -1 : 0);
            ans += (r2 == 2 ? -1 : 0);
        }
        
        return ans;
    }

    int test_hit(xy pos) {
        // Returns:
        //  -1 if out of bounds
        //  0 if not checked
        //  1 if hit
        //  2 if nothing

        auto b = board_.get_board();
        if(pos.first < 0 or pos.first >= n_ or
           pos.second < 0 or pos.second >= n_) {
            return -1;
        }
        char c = b[pos.first][pos.second];
        if(c == '-') {
            return 0;
        } else if (c == 'h') {
            return 1;
        } else {
            return 2;
        }
    }

};


int main() {

    string q;
    cin >> q;
    
    int n = atoi(q.c_str());

    if(n == 0) {

printf("9 9\n"); 
printf("9 8\n");
printf("6 2:7 2\n"); 
printf("3 7:3 8\n");
printf("7 7:7 9\n");
printf("1 2:4 2\n");
printf("5 0:9 0\n");    

//        printf("0 0\n");
//        printf("4 2\n");
//        printf("6 4:7 4\n");
//        printf("3 7:3 8\n"); 
//        printf("7 7:7 9\n");
//        printf("1 4:4 4\n");
//        printf("4 0:8 0\n");
    
    } else {

        Board b(n);
        b.read_board();
    
        ProbabilityPlayer p(b);
        p.move();
    
    }

    return 0;
}




