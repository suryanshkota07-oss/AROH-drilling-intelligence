import type { CommandCenterData } from '../types/domain'

/** Demonstration-only synthetic data; replace with API data when available. */
export const commandCenterDemoData: CommandCenterData = {
  activeWells: [
    { wellId: 'DEMO-AROH-01', name: 'AROH-01', currentDepth: 2930, formation: 'Tipam Sand', status: 'Drilling', riskLevel: 'elevated', location: 'Demo Pad A', rop: 31.8, updatedAt: 'Just now' },
    { wellId: 'DEMO-AROH-02', name: 'AROH-02', currentDepth: 1874, formation: 'Girujan Clay', status: 'Connection', riskLevel: 'watch', location: 'Demo Pad B', rop: 22.4, updatedAt: '2 min ago' },
    { wellId: 'DEMO-AROH-03', name: 'AROH-03', currentDepth: 3462, formation: 'Barail Sandstone', status: 'Circulating', riskLevel: 'normal', location: 'Demo Pad A', rop: 18.9, updatedAt: '3 min ago' },
    { wellId: 'DEMO-AROH-04', name: 'AROH-04', currentDepth: 2618, formation: 'Tipam Sand', status: 'Monitoring', riskLevel: 'critical', location: 'Demo Pad C', rop: 12.7, updatedAt: '1 min ago' },
  ],
  risks: [
    { wellId: 'DEMO-AROH-01', riskScore: 74, severity: 'elevated', eventType: 'Potential loss zone', riskInterval: '2,960–3,020 m', confidence: 78, evidenceCount: 3 },
    { wellId: 'DEMO-AROH-04', riskScore: 91, severity: 'critical', eventType: 'Torque and drag increase', riskInterval: '2,640–2,700 m', confidence: 84, evidenceCount: 4 },
  ],
  recentEvents: [
    { eventId: 'DEMO-EVT-104', wellId: 'DEMO-AROH-04', timestamp: '09:42 UTC', eventType: 'Torque trend elevated', severity: 'critical', depth: 2618, formation: 'Tipam Sand', summary: 'Observed torque trend exceeds the synthetic watch threshold.' },
    { eventId: 'DEMO-EVT-103', wellId: 'DEMO-AROH-01', timestamp: '09:36 UTC', eventType: 'Risk interval approaching', severity: 'elevated', depth: 2930, formation: 'Tipam Sand', summary: 'Current depth is approaching an analogue-derived risk interval.' },
    { eventId: 'DEMO-EVT-102', wellId: 'DEMO-AROH-02', timestamp: '09:28 UTC', eventType: 'Connection complete', severity: 'watch', depth: 1874, formation: 'Girujan Clay', summary: 'Connection completed; telemetry resumed within the demo stream.' },
  ],
  systemHealth: { telemetry: 'Healthy', dataFreshness: '< 30 sec', connectedSources: 4, totalSources: 4 },
}
