describe('Gestor - Agendar Entrevista Individual', () => {
  beforeEach(() => {
    cy.loginGestor();
  });

  it('deve agendar entrevista para um aluno específico', () => {
    cy.visit('/gestor/agendar-entrevista');
    cy.get('select[name="aluno"]').select(1);
    cy.get('input[name="data_hora"]').type('2025-06-20T11:00');
    cy.get('button[type="submit"]').click();
    cy.get('select[name="curso"]').select('1');
    cy.get('input[name="local"]').type('muito');
    cy.get('button[type="submit"]').click();
    cy.contains('Entrevista agendada com sucesso').should('exist');
  });
});