/**
 * Agent Arena widget listing agents and their activity state.
 */
import React from 'react';

export interface Agent {
  name: string;
  active: boolean;
}

export const AgentArena: React.FC<{ agents: Agent[] }> = ({ agents }) => {
  const active = agents.filter((a) => a.active).length;
  return (
    <div className="p-2">
      <h3 className="font-bold">Agents</h3>
      <p>
        {active} / {agents.length} active
      </p>
    </div>
  );
};
