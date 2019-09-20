#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include <math.h>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <climits>
#include <bitset>

#define IOS ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
using namespace std;

typedef pair<int, int> xy;

class Move : public pair<xy, vector<xy>> {

    // each move has a starting point and path to completion
    // it's also efficient to maintain captured pieces, to 
    // 1) alleviate backtracing by the Board class and to
    // 2) easily partition capturing and non-capturing moves.

private:
    
    bool kinged_;
    set<xy> captures_;
     
public:

    Move(xy pos, vector<xy> path, bool kinged=false, set<xy> captures={}) :
    pair<xy, vector<xy>>(pos, path){
        kinged_ = kinged;
        captures_ = captures;
    }
    void print() {
        printf("Move: (%d, %d)", this->first.first, this->first.second);
        for(auto &pos : this->second) {
            printf(" (%d, %d)", pos.first, pos.second);
        }
        printf("\n");
    }
    void perform_move() {
        // just for the game UI
        printf("%lu\n", this->second.size());
        printf("%d %d\n", this->first.first, this->first.second);
        for(auto &pos : this->second) {
            printf("%d %d\n", pos.first, pos.second);
        }
    }
    void grant_king() {kinged_ = true;}
    bool get_kinged() const {return kinged_;}
    void capture(xy pos) { captures_.emplace(pos);}
    void add_one_movement(xy new_pos) {this->second.push_back(new_pos);}
    xy get_shifted_position(int shift) const {
        int n = this->second.size();
        if(n >= shift) {
            return this->second[n-shift];
        } else {
            throw;
        }
    }
    bool has_eaten(xy enemy_pos) const {
        return captures_.find(enemy_pos) != captures_.end();
    }
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

class Piece {
 
    // class for each chekers piece
    // contains x, y coordinates, color, whether the piece is a King
    // and which pieces this piece can attack 

private:

    int i_, j_;
    char color_;
    bool is_king_;
    set<char> can_attack_;
    int direction_;

public: 

    Piece(int i, int j, char player) {
        i_ = i;
        j_ = j;
        color_ = player;
        color_ = (color_ == 'B' ? 'b' : color_);
        color_ = (color_ == 'W' ? 'w' : color_);
        is_king_ = (player == 'B' or player == 'W' ? true : false);
        if(player == 'w' or player == 'W') {
            can_attack_ = {'b', 'B'};
        } else {
            can_attack_ = {'w', 'W'};
        }
        // White discs are present at the bottom of the board and the black 
        // discs are present at the top of the board.
        direction_ = (color_ == 'b' ? 1 : -1);
    }

    char get_color() const {return color_;} 
    bool get_is_king() const {return is_king_;} 
    int get_direction() const {return direction_;}
    int get_i_coordinate() const {return i_;} 
    int get_j_coordinate() const {return j_;} 
    set<char> get_can_attack() const {return can_attack_;}
};

class Board {

  // abstract class for checkers board
  // each board instance will be from the perspective of a single Player
  // Board class need to yield everything a Player might query, including
  // current coordinates of pieces, all legal moves available, forecasting
  // a move, etc. 

private:

    int n_;
    char player_;
    vector<vector<char>> board_;

    // pieces_ tracks a players Peices, not the enemy
    vector<Piece> pieces_;

    // whereas these "pieces" sets are for enemy/ally detection
    set<char> ally_pieces_;
    set<char> enemy_pieces_;

    // for my sanity
    bool debug_ = false;

    void designate_pieces() {
        // seach for ally pieces and initiate them
        for(int i=0; i<n_; i++) {
            for(int j=0; j<n_; j++) {
                if(ally_pieces_.find(board_[i][j]) != ally_pieces_.end()) 
                    pieces_.push_back(Piece(i, j, board_[i][j]));                    
            }
        }        
    }

    void read_board_from_input() {
        board_.resize(n_);
        for(int i=0; i<n_; i++) {
            board_[i].resize(n_);
            for(int j=0; j<n_; j++) {
                cin >> board_[i][j];
            }
        }        
        designate_pieces();    
    }
    
    void read_board_from_string(string& s) {
        board_.resize(n_);
        for(int i=0; i<n_; i++) {
            board_[i].resize(n_);
            for(int j=0; j<n_; j++) {
                board_[i][j] = char(s[i*n_+j]);
            }
        }        
        designate_pieces();    
    }

    void designate_n_and_player(int n, char player) {
        n_ = n;
        player_ = player;
        if(player == 'w' or player == 'W') {
            ally_pieces_ = {'w', 'W'};
            enemy_pieces_ = {'b', 'B'};
        } else {
            ally_pieces_ = {'b', 'B'};
            enemy_pieces_ = {'w', 'W'};
        }
    }

public:

    Board() {}

    Board(int n, char player) {
        designate_n_and_player(n, player);
        read_board_from_input();
    }
    
    Board(int n, char player, string board) {
        designate_n_and_player(n, player);
        read_board_from_string(board);
    }
    
    vector<xy> get_player_positions() const {
        vector<xy> positions;
        for(auto& piece : pieces_) {
            if(piece.get_color() == player_) {
                positions.push_back({piece.get_i_coordinate(), 
                                piece.get_j_coordinate()});
            }
        }
        return positions;
    }

    Moves get_legal_moves() const {
        Moves all_legal_moves;        
        
        // first check attacking moves
        for(auto& piece : pieces_) {
            if(piece.get_color() == player_) {
                auto these_moves =  get_legal_attacking_moves_this_piece(piece);
                if(debug_) {                
                    printf("Just acquired %lu attacking moves from position (%d, %d)\n\n", 
                        these_moves.size(), piece.get_i_coordinate(), piece.get_j_coordinate());    
                }
                all_legal_moves += these_moves;
            }
        }

        // only if there were no attacking moves, look for non-attacking moves
        if(all_legal_moves.size() == 0) {
            for(auto& piece : pieces_) {
                if(piece.get_color() == player_) {
                    auto these_moves = get_legal_non_attacking_moves_this_piece(piece);
                    if(debug_) {                
                        printf("Just acquired %lu non-attacking moves from position (%d, %d)\n\n", 
                            these_moves.size(), piece.get_i_coordinate(), piece.get_j_coordinate());    
                    }
                    all_legal_moves += these_moves;
                }
            }
        }
    
        if(debug_) {
            printf("returning %lu moves\n", all_legal_moves.size());    
        }

        return all_legal_moves;
    }
    
    Moves get_legal_non_attacking_moves_this_piece(Piece piece) const {
        // this is pleasantly simple in comparison
        const int i = piece.get_i_coordinate();
        const int j = piece.get_j_coordinate(); 
        Moves viable_moves_from_here;
        Move empty_move_from_here({i, j}, {});

        vector<int> shifts;
        if(piece.get_is_king()) {
            shifts = {1, -1};
        } else {
            shifts = {piece.get_direction()};
        }

        for(int i_shift : shifts) {
            for(int j_shift : {-1, 1}) {
                xy pos = {i + i_shift, j + j_shift};
                // just make sure we hit an empty space
                if(board_[pos.first][pos.second] == '_') {
                    Move new_move = empty_move_from_here;
                    new_move.add_one_movement(pos);
                    viable_moves_from_here.push_back(new_move);
                }
            }
        }
        return viable_moves_from_here;
    }

    Moves get_legal_attacking_moves_this_piece(Piece piece) const {
        // A directed search is required. each direction could offer
        // branching moves, so it's best to invoke recursion.
        // Let this function be a wrapper for the recursion.

        xy init_last_pos = {-1, -1};
        const int i = piece.get_i_coordinate();
        const int j = piece.get_j_coordinate(); 

        Move empty_move_from_here({i, j}, {});
        Moves initial_moves_from_here = 
            get_single_directed_attacks(piece, i, j, init_last_pos, 
                            empty_move_from_here);
        
        if(debug_) {
            printf("How many initial moves were found? %lu\n", initial_moves_from_here.size());
        }

        Moves all_legal_moves_this_piece;
        for(auto move : initial_moves_from_here) {
            all_legal_moves_this_piece += 
                get_legal_attacking_moves_this_piece_recursive(piece, {i, j}, move); 
        }
        return all_legal_moves_this_piece;
    }

    Moves get_legal_attacking_moves_this_piece_recursive(Piece& piece, 
        xy last_pos, Move& initial_move) const {

        if(debug_) {
            printf("recursing...  ");
            initial_move.print();
        }

        vector<vector<xy>> new_paths;
        xy this_pos = initial_move.get_shifted_position(1);
        if(debug_) {
            printf("just takinga  gander at this pos: (%d, %d) \n", this_pos.first, this_pos.second);
        }   

        Moves moves_from_here = get_single_directed_attacks(piece, 
            this_pos.first, this_pos.second, last_pos, initial_move);
        
//        if(debug_) {
//            printf("successfull jumps to: ");
//            for(auto x : moves_from_here) {
//                printf("(%d, %d) ", x.first, x.second);
//            }
//            printf("\n");
//        }
        
        Moves all_legal_moves_this_piece;
        if(moves_from_here.size() == 0) {
            // thus completes this move, add it to all legal moves and proceed
            all_legal_moves_this_piece.push_back(initial_move);    

        }  else{

            for(auto move : moves_from_here) {
                all_legal_moves_this_piece += 
                    get_legal_attacking_moves_this_piece_recursive(piece, 
                        move.get_shifted_position(2), move);    
            }
        }
        return all_legal_moves_this_piece;
    }

    Moves get_single_directed_attacks(Piece& piece, const int i,
            const int j, xy& last_pos, Move initial_move) const {
        Moves successful_attacking_moves;
        // returns all one-level attack moves, gauranteed to not backtrack to last_pos
        if(piece.get_is_king() or initial_move.get_kinged()) {
            successful_attacking_moves += 
              get_single_directed_attacks_vertically_fixed(piece, -1, i, j, last_pos, initial_move);
            successful_attacking_moves += 
              get_single_directed_attacks_vertically_fixed(piece, 1, i, j, last_pos, initial_move);
        } else {
            int direction = piece.get_direction(); 
            successful_attacking_moves += 
              get_single_directed_attacks_vertically_fixed(piece, direction, i, j, last_pos, initial_move);
        } 
        return successful_attacking_moves;
    }
    
    Moves get_single_directed_attacks_vertically_fixed(Piece& piece, 
        const int direction, const int i, const int j, xy& last_pos, Move initial_move) const {

        // this function needs to update *invididual* moves to monitor capturing and kinging
        
        Moves successful_attacking_moves;
        const auto attackable_pieces = piece.get_can_attack();

        if(debug_) {
            printf("checking %d shifted attacks for moves originating from (%d, %d)\n", direction, i, j);
        }

        for(int j_shift : {-1, 1}) {
            xy pos = {i + 2*direction, j + j_shift*2};
            
            // bound check
            if(not (pos.first < n_ and pos.first >= 0 and 
               pos.second < n_ and pos.second >= 0)) {
                continue;
            }     
             
            // direction check (backtracking prevention) 
//            if(pos.first == last_pos.first and pos.second == last_pos.second) {
//                continue;
//            }
        
            // landing check
            if(board_[pos.first][pos.second] != '_') {
                continue;
            }
            
            if(debug_) {
                printf("shifted to: (%d, %d)\n", pos.first, pos.second);
            }

            // did this actually eat a piece, that was not already eaten?
            xy enemy_pos = {i + direction, j + j_shift};
            if(attackable_pieces.find(board_[enemy_pos.first][enemy_pos.second]) !=
                attackable_pieces.end() and not initial_move.has_eaten(enemy_pos)) {
            
                // create new move, from trunk of old move
                Move new_move = initial_move;
                new_move.add_one_movement(pos);
                new_move.capture(enemy_pos);
                
                // was a King created?
                if(pos.first == 0 or n_-1) {
                    new_move.grant_king();
                }
                if(debug_) {
                    printf("piece eaten!\n");
                }
                successful_attacking_moves.push_back(new_move);
            }
        }
        return successful_attacking_moves;
    }

    void print() {
        for(auto row : board_) {
            for(auto c : row) {
                printf(" %c ", c);
            }
            printf("\n");
        }
    }

};


class Player {

private:
    Board board_;

public:
    Player() {}
    
    Player(Board b) {
        board_ = b;
    }

    void virtual move() {
    }

};

class RandomPlayer : Player {

private:
    Board board_;

public:
    RandomPlayer(Board b) {
        board_ = b;
    }

    void virtual move() {
        auto moves = board_.get_legal_moves();
        moves[rand() % moves.size()].perform_move();        
    }

};

class MiniMaxPlayer : Player {

private:
    Board board_;

public:
    MiniMaxPlayer(Board b) {
        board_ = b;
    }

    void virtual move() {
        auto moves = board_.get_legal_moves();
        moves[rand() % moves.size()].perform_move();        
    }

};

int test_valid_moves1() {

    string test_board = 
        string("________") + 
        string("b_b_b_b_") + 
        string("___b____") +
        string("__b_____") +
        string("_w______") +
        string("w_b___w_") +
        string("_w_____b") +
        string("w_____w_");

    Board b(8, 'w', test_board); 
    auto moves = b.get_legal_moves();
    
    Move answer({6, 1}, {{4, 3}, {2, 1}, {0, 3}, {2, 5}, {0, 7}}); 
    return  moves.size() == 1 and answer == moves[0]; 
}

int test_valid_moves2() {

    string test_board = 
        string("________") + 
        string("________") + 
        string("_w_w____") +
        string("__B_____") +
        string("_w_w____") +
        string("________") +
        string("________") +
        string("________");

    Board b(8, 'b', test_board); 
    auto moves = b.get_legal_moves();
    return  moves.size() == 4; 
}

void tests() {

    int count = 0;
    count += test_valid_moves1();
    count += test_valid_moves2();
    printf("%d/%d test passed\n", count, 2); 

}

int main() {

//    tests();

    char p;
    cin >> p;
    int n;
    cin >> n;
    auto b = Board(n, p);
    RandomPlayer mastermind(b);
    mastermind.move(); 

 
return 0;
}












