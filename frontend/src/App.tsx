import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Feedback from './pages/Feedback'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/feedback" element={<Feedback />} />
      </Routes>
    </BrowserRouter>
  )
}
