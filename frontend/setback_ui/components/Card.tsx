import some from 'lodash/some'
import times from 'lodash/times'
import isNil from 'lodash/isNil'
import styles from './Card.module.scss'

export enum CardSuit {
  Hearts = 0,
  Diamonds = 1,
  Clubs = 2,
  Spades = 3,
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
  const displaySuit = suit => {
    switch (suit) {
      case CardSuit.Hearts:
        return '♥️'
      case CardSuit.Diamonds:
        return '♦️'
      case CardSuit.Clubs:
        return '♣️'
      case CardSuit.Spades:
        return '♠️'
      default:
        return ''
    }
  }
  const redSuits = [CardSuit.Hearts, CardSuit.Diamonds]
  const cardBackStyle = isNil(suit) ? styles.cardBackStyle : ''
  const colorClass = some(redSuits, s => s === suit) ? styles.red : styles.black

  return (
    <div className={`card ${styles.playingCard} ${cardBackStyle}`}>
      <div>
        {times(2, (index) =>
          <div className={styles.cardHalf} key={`cardHalf${index}`}>
            <div className={colorClass}>{displayRank(rank)} {displaySuit(suit)}</div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Card
