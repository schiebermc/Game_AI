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

#define IOS ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
using namespace std;

typedef pair<int, int> xy;

class Move : public pair<xy, vector<xy>> {

    // each move has a starting point and path to completion
    // it's also efficient to maintain captured pieces, to 
    // 1) alleviate backtracing by the Board class and to
    // 2) easily partition capturing and non-capturing moves.

private:
    
    bool kinged_=false;
    set<xy> captures_;
     
public:

    Move(xy pos, vector<xy> path, bool kinged, set<xy> captures={}) :
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
    set<xy> get_captures() { return captures_;}
    void add_one_movement(xy new_pos) {this->second.push_back(new_pos);}
    xy get_origin() const {return this->first;}
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
    char ally_pawn_;
    char ally_king_;
    char enemy_pawn_;
    char enemy_king_;
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
            ally_pawn_ = 'w';
            ally_king_ = 'W';
            enemy_pawn_ = 'b';
            enemy_king_ = 'B';
            ally_pieces_ = {'w', 'W'};
            enemy_pieces_ = {'b', 'B'};
        } else {
            
            ally_pawn_ = 'b';
            ally_king_ = 'B';
            enemy_pawn_ = 'w';
            enemy_king_ = 'W';
            ally_pieces_ = {'b', 'B'};
            enemy_pieces_ = {'w', 'W'};
        }
    
    }

    void set_board(vector<vector<char>> board) {board_ = board; }

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
        Move empty_move_from_here({i, j}, {}, piece.get_is_king());

        vector<int> shifts;
        if(piece.get_is_king()) {
            shifts = {1, -1};
        } else {
            shifts = {piece.get_direction()};
        }

        for(int i_shift : shifts) {
            for(int j_shift : {-1, 1}) {
                
                xy pos = {i + i_shift, j + j_shift};
                Move new_move = empty_move_from_here;
                new_move.add_one_movement(pos);
                
                // bound check
                if(not (pos.first < n_ and pos.first >= 0 and 
                   pos.second < n_ and pos.second >= 0)) {
                    continue;
                }     

                // just make sure we hit an empty space
                if(board_[pos.first][pos.second] != '_') {
                    continue;
                }
        
                // was a King created?
                if(pos.first == 0 or pos.first == n_-1) {
                    new_move.grant_king();
                }
                    
                viable_moves_from_here.push_back(new_move);
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

        Move empty_move_from_here({i, j}, {}, piece.get_is_king());
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
    
        // this function needs to update *invididual* moves to monitor capturing and kinging
        
        Moves successful_attacking_moves;
        const auto attackable_pieces = piece.get_can_attack();

        vector<int> i_shifts;
        if(piece.get_is_king() or initial_move.get_kinged()) {
            i_shifts = {1, -1};
        } else {
            i_shifts = {piece.get_direction()};
        }

        for(int i_shift : i_shifts) {

            if(debug_) {
                printf("checking %d shifted attacks for moves originating from (%d, %d)\n", i_shift, i, j);
            }
        
            for(int j_shift : {-1, 1}) {
                xy pos = {i + 2*i_shift, j + j_shift*2};
                
                // bound check
                if(not (pos.first < n_ and pos.first >= 0 and 
                   pos.second < n_ and pos.second >= 0)) {
                    continue;
                }     
                 
                // landing check
                if(board_[pos.first][pos.second] != '_') {
                    continue;
                }
                
                if(debug_) {
                    printf("shifted to: (%d, %d)\n", pos.first, pos.second);
                }
    
                // did this actually eat a piece, that was not already eaten?
                xy enemy_pos = {i + i_shift, j + j_shift};
                if(attackable_pieces.find(board_[enemy_pos.first][enemy_pos.second]) !=
                    attackable_pieces.end() and not initial_move.has_eaten(enemy_pos)) {
                
                    // create new move, from trunk of old move
                    Move new_move = initial_move;
                    new_move.add_one_movement(pos);
                    new_move.capture(enemy_pos);
                    
                    // was a King created?
                    if(pos.first == 0 or pos.first == n_-1) {
                        new_move.grant_king();
                    }
                    if(debug_) {
                        printf("piece eaten!\n");
                    }
                    successful_attacking_moves.push_back(new_move);
                }
            }
        }
        return successful_attacking_moves;
    }


    Board forecast_move(Move m) {
        
        // copy and modify
        Board new_Board = *this; 
        vector<vector<char>> new_board = board_;

        // remove captured pieces
        for (auto capture : m.get_captures()) {
            new_board[capture.first][capture.second] = '_';
        } 

        // update this piece
        xy origin_pos = m.get_origin();
        xy final_pos = m.get_shifted_position(1); 
        new_board[final_pos.first][final_pos.second] = 
            new_board[origin_pos.first][origin_pos.second];
        new_board[origin_pos.first][origin_pos.second] = '_';

        // did it transform to a king?
        if(m.get_kinged()) {
            new_board[final_pos.first][final_pos.second] = ally_king_; 
        }        

        // finally, assign the board
        new_Board.set_board(new_board);    
        return new_Board; 
    }

    string get_board_string() {
        string s;
        for(auto row : board_) {
            for(auto c : row) {
                s += c;
            }
        }   
        return s;
    }

    void print() {
        for(auto row : board_) {
            for(auto c : row) {
                printf(" %c ", c);
            }
            printf("\n");
        }
    }

    char get_player() {return player_;}

    void switch_perspective() {
        
        // switches the perspective of the board
        // essentially inverts a few data members
        
        player_ = (player_ == 'b' ? 'w' : 'b');
        designate_n_and_player(n_, player_);

        // pieces_ tracks a players Peices, not the enemy
        pieces_.clear();
        designate_pieces();
    }
    
    void switch_perspective_to_player(char player) {
        
        // switches the perspective of the board
        // essentially inverts a few data members
        player_ = player;
        designate_n_and_player(n_, player_);

        // pieces_ tracks a players Peices, not the enemy
        pieces_.clear();
        designate_pieces();
    }
    
    pair<float, float> get_centroid_for_pieces(set<char> pieces) {
        int count = 0;
        float rval = 0.;
        float cval = 0.;
        for(int i=0; i<n_; i++) {
            for(int j=0; j<n_; j++) {
                char c = board_[i][j];
                if(pieces.find(c) != pieces.end()) {
                    rval += i;
                    cval += j;
                    count++;
                }
            }
        }

        pair<float, float> centroid;
        if(count != 0) {
            centroid = {rval / count, cval / count};
        }
        return centroid;
    }   

    friend class BoardEvaluator;

};

class BoardEvaluator : Board {

private:

    bool debug_ = false;
    size_t ally_kings_count_=0;
    size_t ally_pawns_count_=0;
    size_t enemy_pawns_count_=0;
    size_t enemy_kings_count_=0;
    void prepare_utility() {
        for(auto row : board_) {
            for(auto c : row) {
                if(c != '_') {
                    if(ally_pieces_.find(c) != ally_pieces_.end()) {
                        if(c == ally_king_) {
                            ally_kings_count_++;
                        } else {
                            ally_pawns_count_++;
                        }
                    } else {
                        if(c == enemy_king_) {
                            enemy_kings_count_++;
                        } else {
                            enemy_pawns_count_++;
                        }
                    }
                }        
            }
        }
    }

public:

    BoardEvaluator(Board b) : Board(b) {
        prepare_utility();
    }

    float utility() {

        // Here is where the magic happens
        // How does one evaluate the utility of a given checkers board?
        // It might be fairly straightforward.. how many pieces do I have
        // versus how many pieces does the enemy have? Let's also give a 
        // 2x precedence to king pieces.
        float score = (2.*ally_kings_count_ + ally_pawns_count_) - 
                 (2.*enemy_kings_count_ + enemy_pawns_count_);
        
        // however, a win or loss should be exponentiated in value.
        if(ally_kings_count_ + ally_pawns_count_ == 0) {
            score = -100.;
        }

        if(enemy_kings_count_ + enemy_pawns_count_ == 0) {
            score = 100.;
        }

        auto c1 = get_centroid_for_pieces(ally_pieces_);
        auto c2 = get_centroid_for_pieces(enemy_pieces_);

        float dist = sqrt(pow(c1.first - c2.first, 2) + pow(c1.second - c2.second, 2));
        float extra_utility =  (float(n_) - dist) / float(n_) / float(n_);
        
        if(debug_) {
            printf("based on player: %c\n", player_);
            printf("returning utility of %f based on (%zu, %zu) vs (%zu, %zu)\n", score, 
                    ally_kings_count_, ally_pawns_count_, 
                    enemy_kings_count_, enemy_pawns_count_);
        }

        return score;// + extra_utility;
    }

    bool game_over() {
        return enemy_kings_count_ + enemy_pawns_count_ == 0 or 
            ally_kings_count_ + ally_pawns_count_ == 0;
    }

};


class Player {

protected:
    Board board_;
    char player_;

public:
    Player() {}
    
    Player(Board b, char player) {
        board_ = b;
        player_ = player;
    }

    Move virtual get_best_move() {
        return Move({}, {}, false); 
    }

    void move() {
        get_best_move().perform_move();
    }

    friend class RandomPlayer;
    friend class MiniMaxPlayer;
};

class RandomPlayer : public Player {

public:
    RandomPlayer(Board b, char player) : Player(b, player) {
    }

    Move virtual get_best_move() {
        auto moves = board_.get_legal_moves();
        return moves[rand() % moves.size()];
    }

};

class MiniMaxPlayer : public Player {

private:
    size_t depth_;
    bool debug_ = false;

public:
    MiniMaxPlayer(Board b, char player, size_t depth) : Player(b, player) {
        depth_ = depth;
    }

    Move virtual get_best_move() {

        auto stuff = get_best_move_recursive(board_, 1, 1);
        
        if(debug_) {
            printf("final returned utility : %f\n", stuff.second);
        }
        
        return stuff.first;
    }
    
    pair<Move, float> get_best_move_recursive(Board b, int depth, int maximizing, float alpha=FLT_MIN, float beta=FLT_MAX) {

        // minimax search algorithm with alpha beta pruning
        // depth begins as 1 (shown above), if depth == depth, recursion ends
        // maximizing refers to the level of the search tree and which player
        // is in control. 

        if(depth > depth_) {
            throw;
        }        

        // setup search parameters
        float best_utility = (maximizing ? -1000. : 1000.);
        Move best_move({}, {}, false);
        
        for(auto move : b.get_legal_moves()) {
                
            // how good is this subtree?
            Move this_move({}, {}, false);
            float this_utility;

            auto new_board = b.forecast_move(move);
            BoardEvaluator pre_evaluator(new_board);
 
            if(depth < depth_ and not pre_evaluator.game_over()) {
           
                // have to change perspectives so the board knows which
                // player to answer queries for
                new_board.switch_perspective();
 
                auto move_and_utility = get_best_move_recursive(new_board, 
                        depth + 1, 1 - maximizing, alpha, beta);
                this_move = move_and_utility.first;
                this_utility = move_and_utility.second;
            
            } else {
   
                new_board.switch_perspective_to_player(player_);
                BoardEvaluator evaluator(new_board);   
                this_utility = evaluator.utility();
            }            

            if(debug_) {
                move.print();
                printf("depth: %d, maximizing: %d, this_util: %f\n", 
                        depth, maximizing, this_utility);
                if(depth == 1) 
                    printf("\n\n");
            }

            // minimax
            if(maximizing == 1) {
                if(this_utility > best_utility) {
                    best_move = move;
                    best_utility = this_utility;
                    if(debug_) {
                        printf("NEW BEST UTIL! -- %f\n", best_utility);
                    }
                } 
            } else {
                if(this_utility < best_utility) {
                    best_move = move;
                    best_utility = this_utility;
                }
            }

            // alpha-beta pruning - this will greatly decrease the 
            // complexity and allow us to search deeper in less time.
            if(maximizing) {
                alpha = max(alpha, this_utility);
            } else {
                beta = min(beta, this_utility);
            }
            if(alpha >= beta) {
                break;
            }
        }

        return {best_move, best_utility};
    }

};

int play_game(Player a, Player b) {

    
    return 1;
}

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
    
    Move answer({6, 1}, {{4, 3}, {2, 1}, {0, 3}, {2, 5}, {0, 7}}, false); 
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

int test_valid_moves3() {

    string test_board = 
        string("_W_____b") +  
        string("________") + 
        string("_b_b_w_b") + 
        string("______b_") + 
        string("___w___w") + 
        string("________") + 
        string("________") + 
        string("w_w_B_B_"); 

    Board b(8, 'b', test_board); 
    auto moves = b.get_legal_moves();
    return moves.size() == 10;
}

int test_valid_moves4() {

    string test_board = 
        string("___b_b_b") +  
        string("__w___b_") + 
        string("_b_b___b") + 
        string("b_______") + 
        string("_______b") + 
        string("____w_w_") + 
        string("_w_____w") + 
        string("w_w_w_w_"); 

    Board b(8, 'b', test_board); 
    auto moves = b.get_legal_moves();
    Move answer({4, 7}, {{6, 5}}, false); 
    return moves.size() == 1 and  moves[0] == answer;
}

int test_board_forecasting1() {

    string test_board = 
        string("________") + 
        string("_b______") + 
        string("________") +
        string("_b______") +
        string("________") +
        string("_b______") +
        string("w_______") +
        string("________");

    Board b(8, 'w', test_board); 
    auto moves = b.get_legal_moves();
    auto new_board = b.forecast_move(moves[0]);    

    string ans_board = 
        string("__W_____") + 
        string("________") + 
        string("________") +
        string("________") +
        string("________") +
        string("________") +
        string("________") +
        string("________");
    
    string s = new_board.get_board_string();
    return s == ans_board;
}

int test_board_forecasting2() {

    // tests forecasting and evaluation

    string test_board = 
        string("________") + 
        string("_____b__") + 
        string("________") +
        string("_____b__") +
        string("________") +
        string("b__b____") +
        string("__w_____") +
        string("________");

    Board b(8, 'w', test_board);
    auto moves = b.get_legal_moves();
    auto new_board = b.forecast_move(moves[0]);
    BoardEvaluator eval(new_board);
    return eval.utility() - 1. < FLT_EPSILON;
}

int test_switch_perspectives1() {

    string test_board = 
        string("________") + 
        string("________") + 
        string("________") +
        string("________") +
        string("________") +
        string("___b____") +
        string("__w_____") +
        string("________");
    
    Board b(8, 'w', test_board);
    b.switch_perspective(); 
    auto moves = b.get_legal_moves();
    Move answer({6, 2}, {{4, 4}}, false);
    return moves.size() == 1 and moves[0] != answer;
}

int test_switch_perspectives2() {

    string test_board = 
        string("_______W") + 
        string("_w___b__") + 
        string("____b___") +
        string("________") +
        string("w_______") +
        string("___b___w") +
        string("__w_____") +
        string("_____b__");
    
    Board b(8, 'w', test_board);
    BoardEvaluator e1(b);
    b.switch_perspective(); 
    BoardEvaluator e2(b);
    return fabs(e1.utility() - -1*e2.utility()) < FLT_EPSILON;
}

int test_best_move1() {

    string test_board = 
        string("________") + 
        string("_____b__") + 
        string("________") +
        string("_____b__") +
        string("________") +
        string("b__b____") +
        string("__w_____") +
        string("________");

    Board b(8, 'w', test_board);
    bool good = true;
    
    for(int depth=1; depth<=6; depth++) {
        MiniMaxPlayer p(b, 'w', depth);
        for(int i=0; i<10; i++) {
            auto m = p.get_best_move(); 
            Move answer({6, 2}, {{4, 4}, {2, 6}, {0, 4}}, false); 
            good = good and m == answer;
        }
    }

    return good;
}

int test_best_move2() {
        
    // this actually fixed a bug in forecasting
    string test_board = 
        string("___W____") +  
        string("________") + 
        string("________") + 
        string("W_______") + 
        string("________") + 
        string("______b_") + 
        string("_b_b_b__") + 
        string("B_______"); 

    Board b(8, 'b', test_board);
    MiniMaxPlayer p(b, 'b', 1);
    auto m = p.get_best_move(); 
    BoardEvaluator evaluator(b.forecast_move(m));
    return evaluator.utility() == 3;
}

int test_best_move3() {
        
    string test_board = 
        string("___b_b_b") +  
        string("b_b_b_b_") + 
        string("___b____") + 
        string("b_______") + 
        string("_w______") + 
        string("______B_") + 
        string("_w_____b") + 
        string("________"); 

    Board b(8, 'b', test_board);
    MiniMaxPlayer p(b, 'b', 2);
    auto m = p.get_best_move(); 
    Move answer({3, 0}, {{5, 2}, {7, 0}}, true);
    return m == answer;
}

int test_best_move4() {
        
    string test_board = 
        string("_b_b___b") + 
        string("__b_____") +
        string("___b_w_b") +
        string("__b_____") +
        string("___b____") +
        string("________") +
        string("_w_w___w") +
        string("w_w_w_w_");

    Board b(8, 'w', test_board);
    MiniMaxPlayer p(b, 'w', 2);
    auto m = p.get_best_move(); 
    Move answer({2, 5}, {{1, 4}}, false); 
    return m != answer;
}

int test_best_move5() {
        
    string test_board = 
        string("_____b_b") + 
        string("__b_b_b_") + 
        string("___b___b") + 
        string("w_______") + 
        string("________") + 
        string("______w_") + 
        string("_____w_w") + 
        string("__w_w_w_"); 
        
    Board b(8, 'w', test_board);
    MiniMaxPlayer p1(b, 'w', 3);
    auto m1 = p1.get_best_move(); 
    MiniMaxPlayer p2(b, 'w', 2);
    auto m2 = p2.get_best_move(); 
    MiniMaxPlayer p5(b, 'w', 5);
    auto m5 = p5.get_best_move(); 
    return m1 == m2 and m2 == m5;
}

void tests() {

    // pretty manual.. but it works for now
    vector<string> test_names;
    test_names.push_back("test_valid_moves1()");
    test_names.push_back("test_valid_moves2()");
    test_names.push_back("test_valid_moves3()");
    test_names.push_back("test_valid_moves4()");
    test_names.push_back("test_board_forecasting1()");
    test_names.push_back("test_board_forecasting2()");
    test_names.push_back("test_switch_perspectives1()");
    test_names.push_back("test_switch_perspectives2()");
    test_names.push_back("test_best_move1()");
    test_names.push_back("test_best_move2()");
    test_names.push_back("test_best_move3()");
    test_names.push_back("test_best_move4()");
    test_names.push_back("test_best_move5()");
    
    
    vector<int> test_results; 
    test_results.push_back(test_valid_moves1());
    test_results.push_back(test_valid_moves2());
    test_results.push_back(test_valid_moves3());
    test_results.push_back(test_valid_moves4());
    test_results.push_back(test_board_forecasting1());
    test_results.push_back(test_board_forecasting2());
    test_results.push_back(test_switch_perspectives1());
    test_results.push_back(test_switch_perspectives2());
    test_results.push_back(test_best_move1());
    test_results.push_back(test_best_move2());
    test_results.push_back(test_best_move3());
    test_results.push_back(test_best_move4());
    test_results.push_back(test_best_move5());

    int count = 0;
    for(auto x : test_results) {
        count += x;
    }
    
    if(count != test_results.size()) {
        printf("TESTS FAILED!\n"); 
        for(int i=0; i<test_results.size(); i++) {
            if(test_results[i] == 0) {
                printf("    %s - FAILED\n", test_names[i].c_str());
            }
        }
    } else {
        printf("ALL TEST PASS! %d/%d\n", count, count);
    }
}

int main() {


    char p;
    cin >> p;
    int n;
    cin >> n;
    auto b = Board(n, p);
    MiniMaxPlayer mastermind(b, p, 5);
    mastermind.move(); 

//    tests();
 
return 0;
}




