import React, { Component } from 'react'
import Instructions from './Instructions'
import Counter from './Counter'
import Show from './Show'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      shows: [
        {id: 1, name: "Game of Thrones", episodes_seen: 0},
        {id: 2, name: "Naruto", episodes_seen: 220},
        {id: 3, name: "Black Mirror", episodes_seen: 3},
      ],
      value: ''
    }
    this.complete = true;
    this.count = 0;
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    this.setState({shows: this.state.shows.concat([{id: this.state.shows.length + 1, name: this.state.value, episodes_seen: 0}])});
    alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
  }

  // Send a complete prop into the Instructions component that determines whether or not to
  // display a second line of text

  render() {
    const completeProp = this.props
    const countProp = this.props.count
    return (
      <div className="App">
        <Instructions complete={completeProp}/>
        {this.state.shows.map(x => (
          <Show id={x.id} name={x.name} episodes_seen={x.episodes_seen} />
        ))}

        <form onSubmit={this.handleSubmit}>
          <label>
            Show Name:
            <input type="text" value={this.state.value} onChange={this.handleChange} />
          </label>
          <input type="submit" value="Submit" />
        </form>
      </div>
    )
  }
}

export default App
