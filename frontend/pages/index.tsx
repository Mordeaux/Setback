import Head from 'next/head'
import Card, { CardSuit, CardRank } from '../setback_ui/components/Card'
import Hand from '../setback_ui/components/Hand'

export default function Home() {
  return (
    <>
      <Head>
        <title>Setback</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <div className="container">
          <div className="row">
            <div className="col" />
            <div className="col">
              <Hand cards={[
                { rank: CardRank.Ace, suit: CardSuit.Hearts },
                { rank: CardRank.Queen, suit: CardSuit.Hearts },
                { rank: CardRank.Two, suit: CardSuit.Hearts },
                { rank: CardRank.Eight, suit: CardSuit.Spades },
                { rank: CardRank.Nine, suit: CardSuit.Diamonds },
                { rank: CardRank.King, suit: CardSuit.Clubs },
              ]} />
            </div>
            <div className="col" />
          </div>
        </div>
      </main>

      <footer>
      </footer>
    </>
  )
}
