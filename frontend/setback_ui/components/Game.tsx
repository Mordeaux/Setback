import map from 'lodash/map'
import styles from './Game.module.scss'
import Hand from './Hand'
import { HandType } from '../types'
import fetcher from '../../fetcher'

const Game: React.FunctionComponent<{
  hands: HandType[],
}> = ({
  hands,
}) => {
  const { data, error } = fetcher('http://localhost/api')
  if (error) return <div>failed to load</div>
  if (!data) return <div>loading...</div>
  console.log(data)
  return (
    <div className={styles.gameContainer}>
      {map(data.data, ({player, cards}, index) =>
        <Hand
          cards={cards}
          key={player + index}
        />
      )}
    </div>
  )}

export default Game
