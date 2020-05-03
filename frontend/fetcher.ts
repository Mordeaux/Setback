import fetch from 'isomorphic-unfetch'
import useSWR from 'swr'


function fetcher(url) {
  return useSWR(
    url,
    (...args) => fetch(...args).then(response => response.json()),
  )
}

export default fetcher
