
CREATE TRIGGER [dbo].[LXD_LOJA_SAIDAS] ON [dbo].[LOJA_SAIDAS] FOR DELETE NOT FOR REPLICATION AS
-- DELETE trigger on LOJA_SAIDAS
begin
  declare  @errno   int,
           @errmsg  varchar(255)

--- Verifica bloqueio por contagem ------------------------------------------------------------------------------
	IF EXISTS (SELECT 
			Deleted.EMISSAO 
		FROM 
			Deleted 
			INNER JOIN LOJA_SAIDAS_PRODUTO ON Deleted.FILIAL = LOJA_SAIDAS_PRODUTO.FILIAL AND Deleted.ROMANEIO_PRODUTO = LOJA_SAIDAS_PRODUTO.ROMANEIO_PRODUTO 
			INNER JOIN ESTOQUE_PRODUTOS ON ESTOQUE_PRODUTOS.FILIAL = Deleted.FILIAL AND ESTOQUE_PRODUTOS.PRODUTO = LOJA_SAIDAS_PRODUTO.PRODUTO AND ESTOQUE_PRODUTOS.COR_PRODUTO = LOJA_SAIDAS_PRODUTO.COR_PRODUTO 
		WHERE 
			Deleted.EMISSAO < ESTOQUE_PRODUTOS.DATA_AJUSTE)
	BEGIN
		SELECT @errno = 30002, @errmsg = 'N�o � poss�vel excluir movimenta��o de estoque anterior ao ajuste.'
		GOTO Error
	END
-----------------------------------------------------------------------------------------------------------------

--- Verifica sa�da encerrada ------------------------------------------------------------------------------------
	DECLARE @cProduto Char(12), @cCor_Produto Char(10), @cFilial VarChar(25), @nEstoque Int,
		@nEs1  Int, @nEs2  Int, @nEs3  Int, @nEs4  Int, @nEs5  Int, @nEs6  Int, @nEs7  Int, @nEs8  Int,
		@nEs9  Int, @nEs10 Int, @nEs11 Int, @nEs12 Int, @nEs13 Int, @nEs14 Int, @nEs15 Int, @nEs16 Int,
		@nEs17 Int, @nEs18 Int, @nEs19 Int, @nEs20 Int, @nEs21 Int, @nEs22 Int, @nEs23 Int, @nEs24 Int, 
		@nEs25 Int, @nEs26 Int, @nEs27 Int, @nEs28 Int, @nEs29 Int, @nEs30 Int, @nEs31 Int, @nEs32 Int, 
		@nEs33 Int, @nEs34 Int, @nEs35 Int, @nEs36 Int, @nEs37 Int, @nEs38 Int, @nEs39 Int, @nEs40 Int, 
		@nEs41 Int, @nEs42 Int, @nEs43 Int, @nEs44 Int, @nEs45 Int, @nEs46 Int, @nEs47 Int, @nEs48 Int

	DECLARE curSAIDA_ENCERRADA CURSOR FOR 
	SELECT 
		PRODUTO, COR_PRODUTO, DELETED.FILIAL, 
		SUM(EN1) * -1, SUM(EN2) * -1, SUM(EN3) * -1, SUM(EN4) * -1, SUM(EN5) * -1, SUM(EN6) * -1, 
		SUM(EN7) * -1, SUM(EN8) * -1, SUM(EN9) * -1, SUM(EN10) * -1, SUM(EN11) * -1, SUM(EN12) * -1, 
		SUM(EN13) * -1, SUM(EN14) * -1, SUM(EN15) * -1, SUM(EN16) * -1, SUM(EN17) * -1, SUM(EN18) * -1, 
		SUM(EN19) * -1, SUM(EN20) * -1, SUM(EN21) * -1, SUM(EN22) * -1, SUM(EN23) * -1, SUM(EN24) * -1, 
		SUM(EN25) * -1, SUM(EN26) * -1, SUM(EN27) * -1, SUM(EN28) * -1, SUM(EN29) * -1, SUM(EN30) * -1, 
		SUM(EN31) * -1, SUM(EN32) * -1, SUM(EN33) * -1, SUM(EN34) * -1, SUM(EN35) * -1, SUM(EN36) * -1, 
		SUM(EN37) * -1, SUM(EN38) * -1, SUM(EN39) * -1, SUM(EN40) * -1, SUM(EN41) * -1, SUM(EN42) * -1, 
		SUM(EN43) * -1, SUM(EN44) * -1, SUM(EN45) * -1, SUM(EN46) * -1, SUM(EN47) * -1, SUM(EN48) * -1 
	FROM 
		DELETED 
		INNER JOIN LOJA_SAIDAS_PRODUTO ON DELETED.FILIAL = LOJA_SAIDAS_PRODUTO.FILIAL AND DELETED.ROMANEIO_PRODUTO = LOJA_SAIDAS_PRODUTO.ROMANEIO_PRODUTO 
	WHERE
		DELETED.SAIDA_ENCERRADA = 1
	GROUP BY 
		PRODUTO, COR_PRODUTO, DELETED.FILIAL

	OPEN curSAIDA_ENCERRADA

	FETCH NEXT FROM curSAIDA_ENCERRADA INTO @cProduto, @cCor_Produto, @cFilial, 
		@nEs1,  @nEs2,  @nEs3,  @nEs4,  @nEs5,  @nEs6,  @nEs7,  @nEs8,  @nEs9,  @nEs10, @nEs11, @nEs12, 
		@nEs13, @nEs14, @nEs15, @nEs16, @nEs17, @nEs18, @nEs19, @nEs20, @nEs21, @nEs22, @nEs23, @nEs24, 
		@nEs25, @nEs26, @nEs27, @nEs28, @nEs29, @nEs30, @nEs31, @nEs32, @nEs33, @nEs34, @nEs35, @nEs36, 
		@nEs37, @nEs38, @nEs39, @nEs40, @nEs41, @nEs42, @nEs43, @nEs44, @nEs45, @nEs46, @nEs47, @nEs48

	WHILE (@@FETCH_STATUS = 0)
	BEGIN
		SELECT @nEstoque = @nEs1 + @nEs2 + @nEs3 + @nEs4 + @nEs5 + @nEs6 + @nEs7 + @nEs8 + @nEs9 + @nEs10 + @nEs11 + @nEs12 + 
			@nEs13 + @nEs14 + @nEs15 + @nEs16 + @nEs17 + @nEs18 + @nEs19 + @nEs20 + @nEs21 + @nEs22 + @nEs23 + @nEs24 + 
			@nEs25 + @nEs26 + @nEs27 + @nEs28 + @nEs29 + @nEs30 + @nEs31 + @nEs32 + @nEs33 + @nEs34 + @nEs35 + @nEs36 + 
			@nEs37 + @nEs38 + @nEs39 + @nEs40 + @nEs41 + @nEs42 + @nEs43 + @nEs44 + @nEs45 + @nEs46 + @nEs47 + @nEs48

		IF (SELECT COUNT(*) FROM ESTOQUE_PRODUTOS WHERE PRODUTO = @cProduto AND COR_PRODUTO = @cCor_Produto AND FILIAL = @cFilial) > 0
			UPDATE 
				ESTOQUE_PRODUTOS
			SET 
				ESTOQUE = ESTOQUE - @nEstoque, ULTIMA_SAIDA = GETDATE(), 
	            ES1 = ES1 - @nES1, ES2 = ES2 - @nES2, ES3 = ES3 - @nES3, ES4 = ES4 - @nES4, ES5 = ES5 - @nES5, ES6 = ES6 - @nES6, 
	            ES7 = ES7 - @nES7, ES8 = ES8 - @nES8, ES9 = ES9 - @nES9, ES10 = ES10 - @nES10, ES11 = ES11 - @nES11, ES12 = ES12 - @nES12, 
	            ES13 = ES13 - @nES13, ES14 = ES14 - @nES14, ES15 = ES15 - @nES15, ES16 = ES16 - @nES16, ES17 = ES17 - @nES17, ES18 = ES18 - @nES18, 
	            ES19 = ES19 - @nES19, ES20 = ES20 - @nES20, ES21 = ES21 - @nES21, ES22 = ES22 - @nES22, ES23 = ES23 - @nES23, ES24 = ES24 - @nES24, 
	            ES25 = ES25 - @nES25, ES26 = ES26 - @nES26, ES27 = ES27 - @nES27, ES28 = ES28 - @nES28, ES29 = ES29 - @nES29, ES30 = ES30 - @nES30, 
	            ES31 = ES31 - @nES31, ES32 = ES32 - @nES32, ES33 = ES33 - @nES33, ES34 = ES34 - @nES34, ES35 = ES35 - @nES35, ES36 = ES36 - @nES36, 
	            ES37 = ES37 - @nES37, ES38 = ES38 - @nES38, ES39 = ES39 - @nES39, ES40 = ES40 - @nES40, ES41 = ES41 - @nES41, ES42 = ES42 - @nES42, 
	            ES43 = ES43 - @nES43, ES44 = ES44 - @nES44, ES45 = ES45 - @nES45, ES46 = ES46 - @nES46, ES47 = ES47 - @nES47, ES48 = ES48 - @nES48 
			WHERE 
				PRODUTO = @cProduto AND COR_PRODUTO = @cCor_Produto AND FILIAL = @cFilial
		ELSE
			INSERT INTO ESTOQUE_PRODUTOS 
				(PRODUTO, COR_PRODUTO, FILIAL, ESTOQUE, ULTIMA_SAIDA, 
				ES1,  ES2,  ES3,  ES4,  ES5,  ES6,  ES7,  ES8,  ES9,  ES10, ES11, ES12, ES13, ES14, ES15, ES16,  
				ES17, ES18, ES19, ES20, ES21, ES22, ES23, ES24, ES25, ES26, ES27, ES28, ES29, ES30, ES31, ES32,
				ES33, ES34, ES35, ES36, ES37, ES38, ES39, ES40, ES41, ES42, ES43, ES44, ES45, ES46, ES47, ES48)
			VALUES
				(@cProduto, @cCor_Produto, @cFilial, @nEstoque * -1, GETDATE(), 
				@nEs1 * -1, @nEs2 * -1, @nEs3 * -1, @nEs4 * -1, @nEs5 * -1, @nEs6 * -1, @nEs7 * -1, @nEs8 * -1, 
				@nEs9 * -1, @nEs10 * -1, @nEs11 * -1, @nEs12 * -1, @nEs13 * -1, @nEs14 * -1, @nEs15 * -1, @nEs16 * -1, 
				@nEs17 * -1, @nEs18 * -1, @nEs19 * -1, @nEs20 * -1, @nEs21 * -1, @nEs22 * -1, @nEs23 * -1, @nEs24 * -1,
				@nEs25 * -1, @nEs26 * -1, @nEs27 * -1, @nEs28 * -1, @nEs29 * -1, @nEs30 * -1, @nEs31 * -1, @nEs32 * -1,
				@nEs33 * -1, @nEs34 * -1, @nEs35 * -1, @nEs36 * -1, @nEs37 * -1, @nEs38 * -1, @nEs39 * -1, @nEs40 * -1,
				@nEs41 * -1, @nEs42 * -1, @nEs43 * -1, @nEs44 * -1, @nEs45 * -1, @nEs46 * -1, @nEs47 * -1, @nEs48 * -1)
		IF @@ROWCOUNT = 0
		BEGIN
			SELECT @errno = 30002, @errmsg = 'A opera��o foi cancelada. N�o foi poss�vel atualizar "ESTOQUE_PRODUTOS".'
			GOTO Error
		END

		FETCH NEXT FROM curSAIDA_ENCERRADA INTO @cProduto, @cCor_Produto, @cFilial,
			@nEs1,  @nEs2,  @nEs3,  @nEs4,  @nEs5,  @nEs6,  @nEs7,  @nEs8,  @nEs9,  @nEs10, @nEs11, @nEs12, 
			@nEs13, @nEs14, @nEs15, @nEs16, @nEs17, @nEs18, @nEs19, @nEs20, @nEs21, @nEs22, @nEs23, @nEs24, 
			@nEs25, @nEs26, @nEs27, @nEs28, @nEs29, @nEs30, @nEs31, @nEs32, @nEs33, @nEs34, @nEs35, @nEs36, 
			@nEs37, @nEs38, @nEs39, @nEs40, @nEs41, @nEs42, @nEs43, @nEs44, @nEs45, @nEs46, @nEs47, @nEs48
	END

	CLOSE curSAIDA_ENCERRADA
	DEALLOCATE curSAIDA_ENCERRADA

	UPDATE 
		LOJA_SAIDAS_PRODUTO
	SET 
		QTDE_SAIDA = 0, 
		EN1 = 0, EN2 = 0, EN3 = 0, EN4 = 0, EN5 = 0, EN6 = 0, EN7 = 0, EN8 = 0, EN9 = 0, EN10 = 0, EN11 = 0, EN12 = 0, 
		EN13 = 0, EN14 = 0, EN15 = 0, EN16 = 0, EN17 = 0, EN18 = 0, EN19 = 0, EN20 = 0, EN21 = 0, EN22 = 0, EN23 = 0, EN24 = 0, 
		EN25 = 0, EN26 = 0, EN27 = 0, EN28 = 0, EN29 = 0, EN30 = 0, EN31 = 0, EN32 = 0, EN33 = 0, EN34 = 0, EN35 = 0, EN36 = 0, 
		EN37 = 0, EN38 = 0, EN39 = 0, EN40 = 0, EN41 = 0, EN42 = 0, EN43 = 0, EN44 = 0, EN45 = 0, EN46 = 0, EN47 = 0, EN48 = 0 
	FROM 
		DELETED  
		INNER JOIN LOJA_SAIDAS_PRODUTO ON DELETED.ROMANEIO_PRODUTO = LOJA_SAIDAS_PRODUTO.ROMANEIO_PRODUTO AND DELETED.FILIAL = LOJA_SAIDAS_PRODUTO.FILIAL 
	WHERE 
		DELETED.SAIDA_ENCERRADA = 1 

	UPDATE 
		LOJA_SAIDAS_ORIGEM
	SET 
		QTDE_ENTRADA = 0, 
		EN1 = 0, EN2 = 0, EN3 = 0, EN4 = 0, EN5 = 0, EN6 = 0, EN7 = 0, EN8 = 0, EN9 = 0, EN10 = 0, EN11 = 0, EN12 = 0, 
		EN13 = 0, EN14 = 0, EN15 = 0, EN16 = 0, EN17 = 0, EN18 = 0, EN19 = 0, EN20 = 0, EN21 = 0, EN22 = 0, EN23 = 0, EN24 = 0, 
		EN25 = 0, EN26 = 0, EN27 = 0, EN28 = 0, EN29 = 0, EN30 = 0, EN31 = 0, EN32 = 0, EN33 = 0, EN34 = 0, EN35 = 0, EN36 = 0, 
		EN37 = 0, EN38 = 0, EN39 = 0, EN40 = 0, EN41 = 0, EN42 = 0, EN43 = 0, EN44 = 0, EN45 = 0, EN46 = 0, EN47 = 0, EN48 = 0 
	FROM 
		DELETED  
		INNER JOIN LOJA_SAIDAS_ORIGEM ON DELETED.ROMANEIO_PRODUTO = LOJA_SAIDAS_ORIGEM.ROMANEIO_PRODUTO AND DELETED.FILIAL = LOJA_SAIDAS_ORIGEM.FILIAL 
	WHERE 
		DELETED.SAIDA_ENCERRADA = 1 
-----------------------------------------------------------------------------------------------------------------

    /* LOJA_SAIDAS R/1190 LOJA_SAIDAS_PRODUTO ON PARENT DELETE CASCADE */
    delete LOJA_SAIDAS_PRODUTO
      from LOJA_SAIDAS_PRODUTO,deleted
      where
        LOJA_SAIDAS_PRODUTO.ROMANEIO_PRODUTO = deleted.ROMANEIO_PRODUTO and
        LOJA_SAIDAS_PRODUTO.FILIAL = deleted.FILIAL

    delete LOJA_SAIDAS_ORIGEM
      from LOJA_SAIDAS_ORIGEM,deleted
      where
        LOJA_SAIDAS_ORIGEM.ROMANEIO_PRODUTO = deleted.ROMANEIO_PRODUTO and
        LOJA_SAIDAS_ORIGEM.FILIAL = deleted.FILIAL

    return
error:
    raiserror(@errmsg, 18, 1)
    rollback transaction
end
