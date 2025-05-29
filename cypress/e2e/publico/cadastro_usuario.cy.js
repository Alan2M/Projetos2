it('não deve permitir cadastro com email já existente', () => {
  cy.visit('/cadastro/');

  cy.get('input[name="nome"]').type('Usuário Repetido');
  cy.get('input[name="email"]').type('novo@email.com');
  cy.get('input[name="cpf"]').type('123.456.789-00');
  cy.get('input[name="celular"]').type('(81) 91234-5678');
  cy.get('input[name="data-nascimento"]').type('2000-01-01');
  cy.get('select[name="curso"]').select('1');
  cy.get('input[name="senha"]').type('senha123');
  cy.get('input[name="confirmar-senha"]').type('senha123');
  cy.get('button[type="submit"]').click();

  cy.get('.error-message')
    .should('exist')
    .invoke('text')
    .then((text) => {
      cy.log('Mensagem de erro:', text);
      expect(text.trim().length).to.be.greaterThan(0);
    });
});
