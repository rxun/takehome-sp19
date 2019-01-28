import React, { Component } from 'react'
import Counter from './Counter'

// Open the empty Show component which takes a shows id, name, and episodes_seen.
// Display the show name
// Modify the Counter component to take the initial count as a prop, and use this value for count in the initial state.
// Display a Counter (Look how we nested Instructions into App) and pass the number of episodes watched as prop to Counter
// To check that this works, just look at your running app, you should see 3 show names, each of which should have a counter next to it.

class App extends Component {

  render() {
    const showProp = this.props.name
    const episodesProp = this.props.episodes_seen
    return (
      <div>
        This show's name is {showProp}
        <Counter count = {episodesProp}/>
      </div>
    )
  }
}

export default App
