from braink_hr.hr_runtime import HRRuntime, HRAssignment

hr = HRRuntime()
record = HRAssignment(
    assignment_id='assign-r18-001',
    agent_id='agent://braink/runtime/a',
    team_id='team://runtime',
    sector='AI_CLOUD_INFRA',
    roles=('BRAINK_OPERATOR','RUNTIME_ENGINEER'),
    capabilities=('runtime.process','runtime.restart'),
    authority_scope=('KEX://RUNTIME/','vfs://runtime/'),
    verifier=True,
    promoter=False,
)
hr.assign(record)

# G_IDENTITY.identity -> stable agent identity
assert hr.assignments[record.agent_id].agent_id == 'agent://braink/runtime/a'

# G_IDENTITY.role -> declared role set survives assignment and authorization
assert 'BRAINK_OPERATOR' in hr.assignments[record.agent_id].roles

# G_IDENTITY.scope -> target authority scope is enforced by authorize()
ok = hr.authorize('agent://braink/runtime/a','AI_CLOUD_INFRA','runtime.process','KEX://RUNTIME/job/42')
assert ok['authorized'] is True
assert 'BRAINK_OPERATOR' in ok['roles']

out = hr.authorize('agent://braink/runtime/a','AI_CLOUD_INFRA','runtime.process','KEX://DOMAIN/OUTSIDE')
assert out == {'authorized': False, 'reason': 'TARGET_OUT_OF_SCOPE'}

print('HR_GENOME_CAPABILITIES_R18_PASS')
