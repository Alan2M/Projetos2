describe('Gestor - Agendar Vagas', () => {
  beforeEach(() => {
    cy.loginGestor();
  });

  it('deve agendar entrevistas em grupo', () => {
    cy.visit('/gestor/agendar-vagas');
    cy.get('select[name="curso"]').select('1');
    cy.get('input[name="dia_agendamento"]').type('2025-06-20');
    cy.get('input[name="quantidade_alunos"]').type('10');
    cy.get('input[name="periodo"][value="manha"]').type('1');
    cy.get('button[type="submit"]').click();
  });
});