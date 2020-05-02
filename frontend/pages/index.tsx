import Head from 'next/head'
import { CardSuit, CardRank } from '../setback_ui/components/Card'
import Game from '../setback_ui/components/Game'

const hands = [
  {
    player: 'Player 1',
    cards: [
      { },
      { },
      { },
      { },
      { },
      { },
    ],
  },
  {
    player: 'Player 2',
    cards: [
      { rank: CardRank.Ace, suit: CardSuit.Hearts },
      { rank: CardRank.Queen, suit: CardSuit.Hearts },
      { rank: CardRank.Two, suit: CardSuit.Hearts },
      { rank: CardRank.Eight, suit: CardSuit.Spades },
      { rank: CardRank.Nine, suit: CardSuit.Diamonds },
      { rank: CardRank.King, suit: CardSuit.Clubs },
    ],
  },
  {
    player: 'Player 3',
    cards: [
      { },
      { },
      { },
      { },
      { },
      { },
    ],
  },
  {
    player: 'Player 4',
    cards: [
      { },
      { },
      { },
      { },
      { },
      { },
    ],
  },
]

export default function Home() {
  return (
    <>
      <Head>
        <title>Setback</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <Game hands={hands} />
      </main>

      <footer>
      </footer>
    </>
  )
}
