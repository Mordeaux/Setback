import map from 'lodash/map'
import Card, { CardRank, CardSuit } from './Card'
import { CardType } from '../types'
import styles from './Hand.module.scss'

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
        key={`card${index}`}
      />
    )}
  </div>

export default Hand
