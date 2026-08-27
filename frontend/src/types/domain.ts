export type RiskLevel = 'normal' | 'watch' | 'elevated' | 'critical'
export type WellStatus = 'Drilling' | 'Connection' | 'Circulating' | 'Monitoring'
export interface Well { wellId: string; name: string; currentDepth: number; formation: string; status: WellStatus; riskLevel: RiskLevel; location: string; rop: number; updatedAt: string }
export interface Risk { wellId: string; riskScore: number; severity: RiskLevel; eventType: string; riskInterval: string; confidence: number; evidenceCount: number }
export interface DrillingEvent { eventId: string; wellId: string; timestamp: string; eventType: string; severity: RiskLevel; depth: number; formation: string; summary: string }
export interface SystemHealth { telemetry: 'Healthy' | 'Watch'; dataFreshness: string; connectedSources: number; totalSources: number }
export interface CommandCenterData { activeWells: Well[]; risks: Risk[]; recentEvents: DrillingEvent[]; systemHealth: SystemHealth }
