import map from 'lodash/map'
import styles from './Game.module.scss'
import Hand from './Hand'
import { HandType } from '../types'

const Game: React.FunctionComponent<{
  hands: HandType[],
}> = ({
  hands,
}) =>
  <div className={styles.gameContainer}>
    {map(hands, ({player, cards}, index) =>
      <Hand
        cards={cards}
        key={player + index}
      />
    )}
  </div>

export default Game
