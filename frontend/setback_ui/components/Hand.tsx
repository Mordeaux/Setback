import map from 'lodash/map'
import Card, { CardRank, CardSuit } from './Card'
import styles from './Hand.module.scss'

export type CardType = {
  suit: CardSuit,
  rank: CardRank,
}

const Hand: React.FunctionComponent<{
  cards: CardType[],
}> = ({
  cards,
}) =>
  <div className={styles.handContainer}>
    {map(cards, ({suit, rank}, index) =>
      <Card
        suit={suit}
        rank={rank}
        key={rank + suit + index}
      />
    )}
  </div>


export default Hand
