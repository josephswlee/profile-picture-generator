import logo from './logo.svg';
import './App.css';
import Header from './components/Header/Header';
import Hero from './components/Hero/Hero';
import Form from './components/Form/Form';
import View from './components/View/View';

function App() {
  return (
    <div className="App">
      <Hero></Hero>
      <Form></Form>
      {/* <View></View> */}
    </div>
  );
}

export default App;
