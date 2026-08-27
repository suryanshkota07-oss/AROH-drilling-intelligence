import { Outlet } from 'react-router-dom'
import { Header } from './Header'
import { Sidebar } from './Sidebar'
export function AppShell() { return <div className="app-shell"><Sidebar /><div className="app-content"><Header /><main className="page-content"><div className="demo-notice" role="status">DEMO / SYNTHETIC DATA — Not operational OIL data</div><Outlet /></main></div></div> }
