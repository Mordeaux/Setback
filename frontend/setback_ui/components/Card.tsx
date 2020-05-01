import React from 'react'

export enum CardSuit {
  Hearts,
  Diamonds,
  Spades,
  Clubs,
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

const Card: React.FunctionComponent<{
  suit: CardSuit,
  rank: CardRank,
}> = ({
  suit,
  rank,
}) => {
  return (
    <div className="card">
      {suit}
      {rank}
    </div>
  )
}

export default Card
