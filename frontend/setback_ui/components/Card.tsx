import React from 'react'
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
  Ten0,
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
  const colorClass = some(redSuits, s => s === suit) ? styles.red : styles.black

  return (
    <div className={`card ${styles.playingCard}`}>
    <span className={colorClass}>{suit}</span>
      {rank}
    </div>
  )
}

export default Card
