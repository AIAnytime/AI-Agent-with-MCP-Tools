import React from 'react'
import { Workflow, Database, Shield, Cpu, Server, Globe } from 'lucide-react'

function SystemArchitecture() {
  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-6">System Architecture</h2>

      <div className="space-y-8">
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
          <div className="flex items-center space-x-3 mb-4">
            <Workflow className="h-6 w-6 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">Overall System Flow</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg p-4 border-2 border-blue-300">
              <Globe className="h-8 w-8 text-blue-600 mb-2" />
              <h4 className="font-semibold text-sm mb-1">User Interface</h4>
              <p className="text-xs text-gray-600">React frontend with natural language input</p>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-blue-300">
              <Cpu className="h-8 w-8 text-purple-600 mb-2" />
              <h4 className="font-semibold text-sm mb-1">LangChain Agent</h4>
              <p className="text-xs text-gray-600">ReAct Agent with OpenAI GPT-4o</p>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-blue-300">
              <Server className="h-8 w-8 text-green-600 mb-2" />
              <h4 className="font-semibold text-sm mb-1">MCP Server</h4>
              <p className="text-xs text-gray-600">FastAPI with HTTP + SSE</p>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-blue-300">
              <Shield className="h-8 w-8 text-red-600 mb-2" />
              <h4 className="font-semibold text-sm mb-1">RBAC Manager</h4>
              <p className="text-xs text-gray-600">PyCasbin permission control</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">ReAct Agent Operation Flow</h3>
          <div className="space-y-3">
            {[
              { step: 'Question', desc: 'User inputs natural language query', color: 'blue' },
              { step: 'Thought', desc: 'Agent analyzes what action to take', color: 'purple' },
              { step: 'Action Selection', desc: 'Chooses appropriate MCP tool', color: 'green' },
              { step: 'Action Input', desc: 'Prepares parameters for tool execution', color: 'yellow' },
              { step: 'Tool Execution', desc: 'MCP server executes with RBAC check', color: 'red' },
              { step: 'Observation', desc: 'Receives and analyzes result', color: 'indigo' },
              { step: 'Task Complete?', desc: 'Determines if goal is achieved or continues loop', color: 'pink' },
              { step: 'Final Answer', desc: 'Returns result to user', color: 'green' }
            ].map((item, idx) => (
              <div key={idx} className="flex items-center space-x-4">
                <div className={`flex-shrink-0 h-8 w-8 rounded-full bg-${item.color}-100 flex items-center justify-center text-${item.color}-600 font-semibold text-sm`}>
                  {idx + 1}
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{item.step}</div>
                  <div className="text-sm text-gray-600">{item.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Technology Stack</h3>
            <div className="space-y-3">
              <div>
                <div className="text-sm font-medium text-gray-700">Backend</div>
                <div className="text-sm text-gray-600">Python 3.11+, FastAPI, LangChain</div>
              </div>
              <div>
                <div className="text-sm font-medium text-gray-700">AI Model</div>
                <div className="text-sm text-gray-600">OpenAI GPT-4o</div>
              </div>
              <div>
                <div className="text-sm font-medium text-gray-700">RBAC</div>
                <div className="text-sm text-gray-600">PyCasbin</div>
              </div>
              <div>
                <div className="text-sm font-medium text-gray-700">Communication</div>
                <div className="text-sm text-gray-600">HTTP + Server-Sent Events (SSE)</div>
              </div>
              <div>
                <div className="text-sm font-medium text-gray-700">Frontend</div>
                <div className="text-sm text-gray-600">React, TailwindCSS, Vite</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Security Features</h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-2">
                <div className="flex-shrink-0 h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                  <div className="h-2 w-2 bg-green-600 rounded-full"></div>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-900">Principle of Least Privilege</div>
                  <div className="text-xs text-gray-600">Minimum necessary permissions per role</div>
                </div>
              </div>
              <div className="flex items-start space-x-2">
                <div className="flex-shrink-0 h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                  <div className="h-2 w-2 bg-green-600 rounded-full"></div>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-900">Default Deny</div>
                  <div className="text-xs text-gray-600">All operations denied unless explicitly allowed</div>
                </div>
              </div>
              <div className="flex items-start space-x-2">
                <div className="flex-shrink-0 h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                  <div className="h-2 w-2 bg-green-600 rounded-full"></div>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-900">Operation Logging</div>
                  <div className="text-xs text-gray-600">All permission checks and actions logged</div>
                </div>
              </div>
              <div className="flex items-start space-x-2">
                <div className="flex-shrink-0 h-5 w-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                  <div className="h-2 w-2 bg-green-600 rounded-full"></div>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-900">Pre-execution Validation</div>
                  <div className="text-xs text-gray-600">Permissions verified before tool execution</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg p-6 border border-yellow-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Key Benefits</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <div className="text-sm font-medium text-gray-900 mb-1">Security</div>
              <div className="text-xs text-gray-600">Enterprise-grade RBAC prevents unauthorized access</div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-900 mb-1">Flexibility</div>
              <div className="text-xs text-gray-600">Easily extend with new tools and permissions</div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-900 mb-1">Transparency</div>
              <div className="text-xs text-gray-600">Full visibility into agent decisions and actions</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SystemArchitecture
