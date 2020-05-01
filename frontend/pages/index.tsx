import Head from 'next/head'
import Card, { CardSuit, CardRank } from '../setback_ui/components/Card'

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
              <Card
                suit={CardSuit.Hearts}
                rank={CardRank.Ace}
              />
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
