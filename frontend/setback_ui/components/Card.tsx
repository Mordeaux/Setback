import some from 'lodash/some'
import styles from './Card.module.scss'

export enum CardSuit {
  Hearts = '♥️',
  Diamonds = '♦️',
  Spades = '♠️',
  Clubs = '♣️',
}

export enum CardRank {
  Two,
  Three,
  Four,
  Five,
  Six,
  Seven,
  Eight,
  Nine,
  Ten,
  Jack,
  Queen,
  King,
  Ace,
}

const redSuits = [CardSuit.Hearts, CardSuit.Diamonds]

const Card: React.FunctionComponent<{
  suit: CardSuit,
  rank: CardRank,
}> = ({
  suit,
  rank,
}) => {
  const displayRank = rank => {
    if (rank <= CardRank.Ten) {
      return rank + 2
    } else {
      switch (rank) {
        case CardRank.Jack:
          return 'J'
        case CardRank.Queen:
          return 'Q'
        case CardRank.King:
          return 'K'
        case CardRank.Ace:
          return 'A'
      }
    }
  }
  const colorClass = some(redSuits, s => s === suit) ? styles.red : styles.black

  return (
    <div className={`card ${styles.playingCard}`}>
      <div className={styles.rank}>{displayRank(rank)}</div>
      <div className={colorClass}>{suit}</div>
    </div>
  )
}

export default Card
