import { Navigate, Route, Routes } from 'react-router-dom'
import { AppShell } from './components/layout/AppShell'
import { ActiveWellPage } from './pages/ActiveWellPage'
import { CommandCenterPage } from './pages/CommandCenterPage'
import { PlaceholderPage } from './pages/PlaceholderPage'

function App() { return <Routes><Route element={<AppShell />}><Route path="/" element={<Navigate to="/command-center" replace />} /><Route path="/command-center" element={<CommandCenterPage />} /><Route path="/active-well" element={<ActiveWellPage />} /><Route path="/offset-explorer" element={<PlaceholderPage title="Offset Explorer" />} /><Route path="/correlation" element={<PlaceholderPage title="Correlation" />} /><Route path="/knowledge" element={<PlaceholderPage title="Knowledge" />} /><Route path="/copilot" element={<PlaceholderPage title="Copilot" />} /><Route path="*" element={<Navigate to="/command-center" replace />} /></Route></Routes> }

export default App
