import { cleanup, render, screen } from '@testing-library/svelte'
import TeamUsers from '../components/TeamUsers.svelte'
import { describe, it, afterEach, vi, expect } from 'vitest'

const testTeams = [
  { id: 1, name: 'Dev Team', users: [] },
  { id: 2, name: 'QA Team', users: [] }
]

const testUsers = [
  { id: 1, username: 'user1', role: 'developer' },
  { id: 2, username: 'user2', role: 'tester' }
]

describe('TeamUsers.svelte', () => {
  afterEach(() => {
    cleanup()
  })

  it('renders form with team selection, user selection and submit button', () => {
    render(TeamUsers, {
      props: {
        teams: testTeams,
        allUsers: testUsers
      }
    })

    // Verify form elements
    expect(screen.getByLabelText(/Team:/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Users:/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Add Users/i })).toBeInTheDocument()
  })

  it('shows team options from props', () => {
    const { getAllByRole } = render(TeamUsers, {
      props: {
        teams: testTeams,
        allUsers: testUsers
      }
    })

    const options = getAllByRole('option')
    expect(options).toHaveLength(testTeams.length + 1) // Includes default option
    expect(options[1]).toHaveTextContent(testTeams[0].name)
    expect(options[2]).toHaveTextContent(testTeams[1].name)
  })

  it('shows user multi-select options from props', () => {
    const { getAllByRole } = render(TeamUsers, {
      props: {
        teams: testTeams,
        allUsers: testUsers
      }
    })

    const options = getAllByRole('checkbox', { hidden: true })
    expect(options).toHaveLength(testUsers.length)
    expect(options[0]).toHaveAccessibleName(testUsers[0].username)
    expect(options[1]).toHaveAccessibleName(testUsers[1].username)
  })
})