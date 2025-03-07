// @ts-nocheck
import { cleanup, render, screen, fireEvent } from '@testing-library/svelte'
import TeamUsers from '../components/TeamUsers.svelte'
import { post } from '../utils/api'
import { describe, it, afterEach, vi, expect } from 'vitest'

vi.mock('../utils/api.js')

const testTeams = [
  { id: 1, name: 'Dev Team' },
  { id: 2, name: 'QA Team' }
]

const testUsers = [
  { id: 11, username: 'userA' },
  { id: 22, username: 'userB' }
]

describe('TeamUsers Form Submission', () => {
  afterEach(() => {
    cleanup()
    vi.clearAllMocks()
  })

  it('submits selected team and users to API', async () => {
    post.mockResolvedValue({ ok: true })

    const { getByLabelText, getByRole } = render(TeamUsers, {
      props: { teams: testTeams, allUsers: testUsers }
    })

    // Select team and users
    await fireEvent.change(getByLabelText(/Team:/), { target: { value: '1' } })
    await fireEvent.click(getByLabelText('userA'))
    await fireEvent.click(getByLabelText('userB'))

    // Submit form
    await fireEvent.submit(getByRole('button', { name: /Add Users/i }))

    // Verify API call
    expect(post).toHaveBeenCalledWith(
      '/teams/1/users',
      { user_ids: [11, 22] }
    )
  })

  it('shows error message on API failure', async () => {
    post.mockResolvedValue({ ok: false, status: 500, json: () => Promise.resolve({ message: 'Error adding users' }) })

    const { getByLabelText, getByRole, findByText } = render(TeamUsers, {
      props: { teams: testTeams, allUsers: testUsers }
    })

    await fireEvent.change(getByLabelText(/Team:/), { target: { value: '2' } })
    await fireEvent.click(getByLabelText('userA'))
    await fireEvent.submit(getByRole('button', { name: /Add Users/i }))

    expect(await findByText(/Error adding users/i)).toBeInTheDocument()
  })
})
