/**
 * TypeScript types for Atlas workspace data structures
 */

export type WorkspaceType = 
  | "travel_research"
  | "purchase_research"
  | "learning_plan"
  | "project_planner";

export interface Module {
  type: string;
}

export interface SourceQueries {
  maps?: string[];
  reddit?: string[];
  youtube?: string[];
  web?: string[];
  academic?: string[];
}

export interface WorkspaceSchema {
  title: string;
  modules: Module[];
  recommended_sources: string[];
  source_queries: SourceQueries;
}

export interface Evidence {
  source: string;
  label: string;
  url: string;
}

export interface Suggestion {
  title: string;
  category: string;
  reason: string;
  evidence: Evidence[];
  actions: string[];
}

export interface SavedItem {
  type: string;
  title: string;
  notes?: string;
  links?: string[];
  tags?: string[];
}

export interface Workspace {
  id: string;
  query: string;
  workspace_type: WorkspaceType;
  schema?: WorkspaceSchema;
  modules: Module[];
  enabled_sources: string[];
  suggestions: Suggestion[];
  saved_items: SavedItem[];
}
