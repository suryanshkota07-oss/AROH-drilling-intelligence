export type RiskLevel = 'normal' | 'watch' | 'elevated' | 'critical'
export type WellStatus = 'Drilling' | 'Connection' | 'Circulating' | 'Monitoring'
export interface Well { wellId: string; name: string; currentDepth: number; formation: string; status: WellStatus; riskLevel: RiskLevel; location: string; rop: number; updatedAt: string }
export interface Risk { wellId: string; riskScore: number; severity: RiskLevel; eventType: string; riskInterval: string; confidence: number; evidenceCount: number }
export interface DrillingEvent { eventId: string; wellId: string; timestamp: string; eventType: string; severity: RiskLevel; depth: number; formation: string; summary: string }
export interface SystemHealth { telemetry: 'Healthy' | 'Watch'; dataFreshness: string; connectedSources: number; totalSources: number }
export interface CommandCenterData { activeWells: Well[]; risks: Risk[]; recentEvents: DrillingEvent[]; systemHealth: SystemHealth }
export interface DepthRiskPoint { depth: number; riskScore: number }
export interface DepthRiskTimeline { currentDepth: number; riskStartDepth: number; riskEndDepth: number; points: DepthRiskPoint[] }
export interface RiskReason { label: string; detail: string; strength: 'high' | 'moderate' }
export interface OffsetEvidence { wellId: string; depth: number; formation: string; historicalEvent: string; severity: RiskLevel; outcome: string }
export interface DrillingParameter { label: string; value: number; unit: string; trend: 'rising' | 'stable' | 'falling'; detail: string }
export interface RecommendedAction { title: string; action: string; rationale: string }
export interface ActiveWellData { well: Well; risk: Risk; depthTimeline: DepthRiskTimeline; reasons: RiskReason[]; offsetEvidence: OffsetEvidence[]; parameters: DrillingParameter[]; recentEvents: DrillingEvent[]; recommendedAction: RecommendedAction }
