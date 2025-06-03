describe('Admin -  Professor', () => {
  beforeEach(() => {
    cy.visit('/admin');
    cy.get('input[name="username"]').type('admin');
    cy.get('input[name="password"]').type('123');
    cy.get('input[type="submit"]').click();
    cy.visit('/gestor/inicio');
  });

  it('deve acessar a tela de adicionar gestor', () => {

    const timestamp = Date.now();
    cy.get('input[name="username"]').type(`user${timestamp}`);
    cy.get('input[name="email"]').type(`user${timestamp}@teste.com`);    
    cy.get('input[name="senha"]').type('senha123');
    cy.get('button[type="submit"]').click();
    cy.contains('Gestor criado com sucesso').should('exist');

  });
});
