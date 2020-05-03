import Head from 'next/head'
import { CardSuit, CardRank } from '../setback_ui/components/Card'
import Game from '../setback_ui/components/Game'

export default function Home() {
  return (
    <>
      <Head>
        <title>Setback</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <Game />
      </main>

      <footer>
      </footer>
    </>
  )
}
