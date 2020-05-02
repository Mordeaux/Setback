
export type CardType = {
  suit: CardSuit,
  rank: CardRank,
}

export type HandType = {
  cards: [CardType, {}]>,
  player: string,
}
