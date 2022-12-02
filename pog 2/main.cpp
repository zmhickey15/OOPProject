
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fstream>

#include <iostream>


using namespace std;

int p1hand, p2hand, p3hand, p4hand, turn;

void writeToLog( const string &text )
{
  fstream log_file;
  //log_file.open("log.txt");
    log_file.open("log.txt", ios_base::out | ios_base::app );
    log_file << text << endl;
    log_file.close();
}


enum Suit {club = 0, heart = 1, spade = 2, diamond = 3  };
struct Card {
  int num;  // card number 
  enum Suit suit; // card suit 
};

class Deck
{
    int deckSize = 52;
    int size;
    Card *cards = new Card[deckSize];

public:
    Deck();
    void shuffle();
    void push(Card);
    void draw();
    void show();
    Card topCard();
};
// create deck 
Deck::Deck() : size(deckSize-1)
{
    srand (time(NULL));
    int cnt = 0;
    Suit s;
    // set suit 
    for (int i = 0; i < 4; ++i) {
        switch (i) {
            case 0: s = club; break;
            case 1: s = heart; break;
            case 2: s = spade; break;
            case 3: s = diamond; break;
            default: cerr << "invalid suit";
        }
        // give cards values ace = 0 ... k = 13
        for (int j = 0; j < 13; ++j) {
            cards[cnt].num = j;
            cards[cnt].suit = s;
            cnt++;
        }
    }
}

// shuffle deck 
void Deck::shuffle()
{
    Card *tmp = new Card[deckSize-1];
    int tmpSize = 0;
    bool shuffled = false;
    int j = 0;
    while (!shuffled)
    {
        int k = 0;
        while (k < 1 || k > deckSize)
            k = rand() % deckSize + 1;
        Card c = cards[k];
        bool contains = false;
        for (int i = 0; i < tmpSize; ++i) {
            if (tmp[i].num == c.num && tmp[i].suit == c.suit) {
                contains = true;
                break;
            }
        }
        // make sure not in deck 
        if (!contains) {
            tmp[j] = c;
            j++;
            tmpSize++;
        // all kards in 
            if (j == deckSize-1) shuffled = true;
        }
    }
    delete[] cards;
    cards = tmp;
}

// get top card 
void Deck::draw()
{
    Card *tmp = new Card[deckSize-1];
    for (int i = 0; i < size; ++i)
        tmp[i] = cards[i+1];
    delete[] cards;
    cards = tmp;
    size--;
}
Card Deck::topCard() { return cards[0]; }

// put card on top
void Deck::push(Card c)
{
    cards[size] = c;
    size++;
    //show();
}

// print deck to consule 
void Deck::show()
{
 string info;
  for (int k = 0; k < deckSize; k++){
    cout << cards[k].num <<" ";
     info += to_string(cards[k].num ) + "  ";
    
  }
  writeToLog(info);
}


// player class /////////////////////////////
class Player{
  private:
    int num;
    int FULL_HAND = 2; // can have 2 cards at a time
    int handSize; // how many cards in hand 
   
    bool winner; // plauyer won

  public:
    Player(int);
    int team;
    Card* hand;
    void draw(Card);
    bool isWinner();
    bool isTurn();
    void exit();
    //void out();
    int getHand();
    Card discard();
    void printHand();
    void setTeam(int n);

};
// create player 
Player::Player(int n):num(n), handSize(0), winner(false)
{
    hand = new Card[2];
}
// set team 
void Player::setTeam( int n){
  team = n;
}

int Player::getHand(){return hand[0].num; }

// draw card
void Player::draw(Card card)
{
    hand[handSize] = card;
    handSize++;
    string info = "player " + to_string(team) + " draws " + to_string(card.num);
    writeToLog(info);
}

// discard card
Card Player::discard()
{
    Card *tmpHand = new Card[2];
    int i = rand() % FULL_HAND;
    Card remove = hand[i];
    Card keep;
    if (i == 0) keep = hand[1];
    else keep = hand[0];

    tmpHand[0] = keep;
    delete[] hand;
    hand = tmpHand;
    handSize = 1;
    cout <<endl<< "discarded " + to_string(remove.num) << " at random"<<endl;
    string info = "discarded " + to_string(remove.num) + " at random";
    writeToLog(info);

    if(team == 1 )
      p1hand = getHand();
    if (team == 2)
      p2hand = getHand();
    if (team == 3)
      p3hand = getHand();
    if (team == 4)
      p4hand = getHand();
    //cout <<"still in hand " <<getHand() <<endl;


    return remove;
}

// check if team won
bool Player::isWinner(){

    if( team == 1 && (p3hand == hand[0].num || p3hand == hand[1].num) ){
      winner = true;
      cout << " player 2 has: " << p3hand << endl <<"player 1: team 1 wins"<<endl;
      string info = "player 2 has: " + to_string(p3hand) + "\nplayer 1: team 1 wins";
      writeToLog(info);

      return true;
    }else if( team == 2 && (p4hand == hand[0].num || p4hand == hand[1].num) ){
        winner = true;
        cout << " player 4 has: " << p4hand << endl <<"player 2: team 2 wins"<<endl;
        string info = "player 4 has: " + to_string(p4hand) + "\nplayer 2: team 2 wins";
        writeToLog(info);
        return true;
    }else if( team == 3 && (p1hand == hand[0].num || p1hand == hand[1].num) ){
        winner = true;
        cout << " player 1 has: " << p1hand << endl <<"player 3: team 1 wins"<<endl;
              string info = "player 1 has: " + to_string(p1hand) + "\nplayer 3: team 1 wins";
      writeToLog(info);
        return true;
    }else if( team == 4 && (p2hand == hand[0].num || p2hand == hand[1].num) ){
        winner = true;
        cout << " player 1 has: " << p2hand << endl <<"player 4: team 2 wins"<<endl;
        string info = "player 1 has: " + to_string(p2hand) + "\nplayer 4: team 1 wins";
      writeToLog(info);
        return true;
    }
     

    else {
      winner = false;
      return false;
    }
  
}

// print hand 
void Player::printHand(){
      string str;
    for (int i = 0; i < handSize; ++i) {
        if (i == 0) str = to_string(hand[i].num);
        else str += " " + to_string(hand[i].num);
    }
    cout<<"PLAYER:" <<team<< " HAND " + str;
    string info = "player " + to_string(team) + " HAND " + str;
    writeToLog(info);
}


void Player::exit(){
  cout << "player " <<team << " exits" <<endl;
  string info = "player " + to_string(team) + " exits";
      writeToLog(info);
}

bool Player::isTurn(){
   int playerToGo;

   playerToGo = turn % 4;

  if( (team == 1 && playerToGo == 1) )
    return true;
  if( (team == 2 && playerToGo == 2) )
    return true;
  if( (team == 3 && playerToGo == 3) )
    return true;
  if( (team == 4 && playerToGo == 0) )
    return true;


  return false;
}


// dealer class //////////////////////////
class Dealer
{
    Card hand;

public:
    Dealer();
    Card deal();
    void draw(Card);
};

Dealer::Dealer() {}

Card Dealer::deal() { return hand; }

void Dealer::draw(Card card) { hand = card; }

Deck deck;  //shared data for all threads
bool winner;
pthread_mutex_t player_mutex;
pthread_cond_t winnerExists;
pthread_t dlr, player1, player2, player3, player4;




struct thread_data // what will be put in wach thred 
{
    int  thread_id; //integer value to name the player (1, 2, or 3)
    Card card;      //the first card dealt to player by the dealer
    int team; // player team
};



void *Play(void *param)
{
    auto *arg = (thread_data *)param;   //cast param to thread_data structure
    Player player(arg->thread_id);      //create player object with thread id
    player.setTeam(arg -> team);
    player.draw(arg->card);             //add card to players hand
 

    // set starting hands
    if(player.team == 1 )
      p1hand = player.getHand();
    if (player.team == 2)
      p2hand = player.getHand();
    if (player.team == 3)
      p3hand = player.getHand();
    if (player.team == 4)
      p4hand = player.getHand();

    while (!winner)
    {
    if(player.isTurn()) { 
      pthread_mutex_lock(&player_mutex);
      
        player.printHand();
        cout <<endl;


        player.draw(deck.topCard());
        deck.draw();
        player.printHand();
        
        if (player.isWinner()) {
            winner = true;
           // player.exit();
 
            pthread_cond_signal(&winnerExists);
        } else {
            deck.push(player.discard());
        }
        cout <<"Deck: ";

        
        deck.show();

        cout <<endl;
        turn++;
        
        

        pthread_mutex_unlock(&player_mutex);

        /* Do some "work" so threads can alternate on _mutex lock */


        sleep(1);
    }

    }
    pthread_mutex_lock(&player_mutex);

    player.exit();
    
    pthread_mutex_unlock(&player_mutex);

}

void *_dealer(void *param)
{
    auto *arg = (thread_data *)param;   //cast param to thread_data structure
    auto myID = arg->thread_id;
    /**
     * Lock mutex and wait for signal.
     */
    pthread_mutex_lock(&player_mutex);
    while(!winner)
    {
        pthread_cond_wait(&winnerExists, &player_mutex);
        //cout << "Winner exists.\n";
    }
    pthread_mutex_unlock(&player_mutex);

}


int main(){
  turn = 1;

    fstream log_file;
  //log_file.open("log.txt");
    log_file.open("log.txt", ios_base::out | ios_base::trunc );
    log_file.close();
  for (int k = 1; k < 3; k++){
    deck = Deck();
    turn = k;
    winner = false;
    cout<< endl << "ROUND " << k << endl;
        string info = "\nROUND  " + to_string(k) + " \n";
    writeToLog(info);


        deck.shuffle();
        Dealer dealer;
    cout<< "DEALER: shuffle " << endl;
         info = "DEALER: shuffle\n";
        writeToLog(info);
        
        thread_data d;
        d.thread_id = 5;

        // create the thread_data with the thread ID and the first card
        thread_data td[4];
        for (int i = 0; i < 4; ++i) {
            td[i].thread_id = i+1;
            dealer.draw(deck.topCard());
            td[i].card = dealer.deal();
            td[i].team = i+1;
            deck.draw();
        }

        //deck.show();

        /* Initialize mutex and condition variable objects */
        pthread_mutex_init(&player_mutex, nullptr);
        pthread_cond_init (&winnerExists, nullptr);

        /* Create threads */
        pthread_create(&dlr, nullptr, _dealer, (void *) &d);
        pthread_create(&player1, nullptr, Play, (void *) &td[0]);
        pthread_create(&player2, nullptr, Play, (void *) &td[1]);
        pthread_create(&player3, nullptr, Play, (void *) &td[2]);
        pthread_create(&player4, nullptr, Play, (void *) &td[3]);
        /* Wait for all threads to complete */
        pthread_join(player1, nullptr);
        pthread_join(player2, nullptr);
        pthread_join(player3, nullptr);
        pthread_join(player4, nullptr);

  }
}
