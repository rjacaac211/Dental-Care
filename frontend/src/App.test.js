import { render, screen } from '@testing-library/react';
import App from './App';

test('renders navbar with RJ Dental Care PH', () => {
  render(<App />);
  const navbarElement = screen.getByText(/RJ Dental Care PH/i);
  expect(navbarElement).toBeInTheDocument();
});
